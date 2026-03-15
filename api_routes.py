"""
REST API for the D&D Campaign Manager.

Provides programmatic access to game state, actions, combat, diagnostics,
and Discord integration. Authenticated via API key in the Authorization header.

Usage:
  curl -H "Authorization: Bearer <CLAUDE_API_KEY>" https://questerledger.johnbest.ai/api/campaigns
"""

import json
import os
import traceback
from datetime import datetime
from functools import wraps

from flask import Blueprint, jsonify, request

from models import db, User, Character, Campaign, DiceRoller

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ── Auth ────────────────────────────────────────────────────

def require_api_key(f):
    """Decorator: require valid API key in Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        key = os.environ.get('CLAUDE_API_KEY', '')
        if not key:
            return jsonify(error="API not configured — set CLAUDE_API_KEY in .env"), 503
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '').strip()
        if token != key:
            return jsonify(error="Unauthorized"), 401
        return f(*args, **kwargs)
    return decorated


# ── Helper ──────────────────────────────────────────────────

def _campaign_json(c):
    """Serialize a Campaign for API responses."""
    chars = Character.query.filter_by(campaign_id=c.id).all()
    state = c.current_state or {}
    return {
        'id': c.id,
        'name': c.name,
        'join_code': c.join_code,
        'is_active': c.is_active,
        'dm_id': c.dm_id,
        'player_ids': c.players or [],
        'characters': [_char_json(ch) for ch in chars],
        'npcs': [
            npc for npc in (state.get('initiative_order') or [])
            if npc.get('is_npc')
        ],
        'combat_active': state.get('combat_active', False),
        'round': state.get('round', 0),
        'turn_index': state.get('turn_index', 0),
        'initiative_order': state.get('initiative_order', []),
        'active_conditions': state.get('active_conditions', {}),
        'discord': state.get('discord', {}),
        'narration_log': (state.get('narration_log') or [])[-20:],
        'combat_log': (state.get('combat_log') or [])[-30:],
        'sms_log': (state.get('sms_log') or [])[-20:],
    }


def _char_json(ch):
    """Serialize a Character for API responses."""
    return {
        'id': ch.id,
        'name': ch.name,
        'race': ch.race,
        'class_name': ch.class_name,
        'level': ch.level,
        'hp_current': ch.hp_current,
        'hp_max': ch.hp_max,
        'ac': ch.ac,
        'ability_scores': ch.ability_scores or {},
        'proficiency_bonus': ch.proficiency_bonus,
        'skills': ch.skills or [],
        'equipment': ch.equipment or [],
        'spells': ch.spells or {},
        'background': ch.background,
        'alignment': ch.alignment,
        'campaign_id': ch.campaign_id,
        'user_id': ch.user_id,
    }


def _get_campaign_or_404(campaign_id):
    c = Campaign.query.get(campaign_id)
    if not c:
        return None, (jsonify(error=f"Campaign {campaign_id} not found"), 404)
    return c, None


def _save_state(campaign):
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(campaign, 'current_state')
    db.session.commit()


def _log_action(campaign, actor, action_type, text):
    """Append to the campaign's combat log."""
    state = campaign.current_state or {}
    log = state.setdefault('combat_log', [])
    log.append({
        'type': action_type,
        'actor': actor,
        'text': text,
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'api',
    })
    if len(log) > 200:
        state['combat_log'] = log[-200:]
    campaign.current_state = state
    _save_state(campaign)


def _post_debug(campaign, message):
    """Post a message to the campaign's Discord debug channel."""
    try:
        from services.discord_bot import bot, _bot_loop
        if not _bot_loop or not bot.is_ready():
            return
        state = campaign.current_state or {}
        discord_cfg = state.get('discord', {})
        debug_id = discord_cfg.get('channels', {}).get('debug')
        if not debug_id:
            return
        import asyncio

        async def _send():
            ch = bot.get_channel(int(debug_id))
            if ch:
                # Truncate to Discord's 2000 char limit
                msg = message[:1990]
                await ch.send(f"```\n{msg}\n```")

        asyncio.run_coroutine_threadsafe(_send(), _bot_loop)
    except Exception:
        pass  # debug channel is best-effort


# ══════════════════════════════════════════════════════════════
# CAMPAIGN ENDPOINTS
# ══════════════════════════════════════════════════════════════

@api_bp.route('/campaigns', methods=['GET'])
@require_api_key
def list_campaigns():
    """List all campaigns (optionally filter by active)."""
    active_only = request.args.get('active', 'true').lower() == 'true'
    q = Campaign.query
    if active_only:
        q = q.filter_by(is_active=True)
    campaigns = q.all()
    return jsonify(campaigns=[_campaign_json(c) for c in campaigns])


@api_bp.route('/campaigns/<int:cid>', methods=['GET'])
@require_api_key
def get_campaign(cid):
    """Full campaign state."""
    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    return jsonify(campaign=_campaign_json(c))


@api_bp.route('/characters/<int:char_id>', methods=['GET'])
@require_api_key
def get_character(char_id):
    """Full character sheet."""
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404
    return jsonify(character=_char_json(ch))


# ══════════════════════════════════════════════════════════════
# GAME ACTIONS
# ══════════════════════════════════════════════════════════════

@api_bp.route('/action', methods=['POST'])
@require_api_key
def api_action():
    """
    Process a natural-language action through the AI DM pipeline.

    Body: {campaign_id, character_id, message}
    The AI interprets intent, resolves mechanics, and narrates the result.
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    char_id = data.get('character_id')
    message = data.get('message', '')

    if not cid or not char_id or not message:
        return jsonify(error="Required: campaign_id, character_id, message"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    from services.ai_dm import process_player_sms
    _post_debug(c, f"[API] action from {ch.name}: {message}")

    try:
        response = process_player_sms(message, ch, c)
    except Exception as e:
        _post_debug(c, f"[API] action error: {e}")
        return jsonify(error=str(e)), 500

    # Bridge to Discord
    try:
        from services.discord_bot import post_to_discord
        post_to_discord(c, ch.name, message, response, source="api")
    except Exception:
        pass

    _post_debug(c, f"[API] response: {response[:200]}")
    return jsonify(character=ch.name, message=message, response=response)


@api_bp.route('/roll', methods=['POST'])
@require_api_key
def api_roll():
    """
    Roll dice.

    Body: {dice, campaign_id (optional)}
    Example: {dice: "2d6+3"}
    """
    data = request.get_json(force=True)
    dice_str = data.get('dice', '')
    cid = data.get('campaign_id')

    if not dice_str:
        return jsonify(error="Required: dice"), 400

    from services.engine import resolve_roll
    result = resolve_roll(dice_str)
    if 'error' in result:
        return jsonify(error=result['error']), 400

    if cid:
        c = Campaign.query.get(cid)
        if c:
            _log_action(c, 'API', 'roll', result['text'])
            _post_debug(c, f"[API] roll {dice_str}: {result['text']}")

    return jsonify(result=result)


@api_bp.route('/skill-check', methods=['POST'])
@require_api_key
def api_skill_check():
    """
    Resolve a skill check.

    Body: {campaign_id, character_id, skill}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    char_id = data.get('character_id')
    skill = data.get('skill', '')

    if not all([cid, char_id, skill]):
        return jsonify(error="Required: campaign_id, character_id, skill"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    from services.engine import resolve_skill_check
    result = resolve_skill_check(ch, c, skill)
    if 'error' in result:
        return jsonify(error=result['error']), 400

    _log_action(c, ch.name, 'skill_check', result['text'])
    _post_debug(c, f"[API] {ch.name} skill check {skill}: {result['text']}")
    return jsonify(character=ch.name, result=result)


@api_bp.route('/attack', methods=['POST'])
@require_api_key
def api_attack():
    """
    Resolve an attack.

    Body: {campaign_id, character_id, target, ability (optional), damage_dice (optional)}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    char_id = data.get('character_id')
    target = data.get('target', 'target')
    ability = data.get('ability', 'STR')
    damage_dice = data.get('damage_dice')

    if not all([cid, char_id]):
        return jsonify(error="Required: campaign_id, character_id"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    from services.engine import resolve_attack
    result = resolve_attack(ch, c, target, ability, damage_dice)

    _log_action(c, ch.name, 'attack', result['text'])
    _post_debug(c, f"[API] {ch.name} attacks {target}: {result['text']}")

    # Apply damage to NPC if hit
    if result.get('hit') and result.get('damage_total'):
        from services.engine import apply_damage_to_npc
        dmg_result = apply_damage_to_npc(c, target, result['damage_total'])
        if 'error' not in dmg_result:
            result['npc_hp'] = dmg_result

    return jsonify(character=ch.name, result=result)


@api_bp.route('/saving-throw', methods=['POST'])
@require_api_key
def api_saving_throw():
    """
    Resolve a saving throw.

    Body: {character_id, ability}
    """
    data = request.get_json(force=True)
    char_id = data.get('character_id')
    ability = data.get('ability', '')

    if not all([char_id, ability]):
        return jsonify(error="Required: character_id, ability"), 400

    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    from services.engine import resolve_saving_throw
    result = resolve_saving_throw(ch, ability)
    if 'error' in result:
        return jsonify(error=result['error']), 400

    return jsonify(character=ch.name, result=result)


# ══════════════════════════════════════════════════════════════
# SCENE & NARRATION
# ══════════════════════════════════════════════════════════════

@api_bp.route('/scene', methods=['POST'])
@require_api_key
def api_scene():
    """
    Set a scene / post narration.

    Body: {campaign_id, text}
    Posts to narration log and Discord tavern channel.
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    text = data.get('text', '')

    if not cid or not text:
        return jsonify(error="Required: campaign_id, text"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    # Add to narration log
    state = c.current_state or {}
    narr = state.setdefault('narration_log', [])
    narr.append({'text': text, 'timestamp': datetime.utcnow().isoformat(), 'source': 'api'})
    if len(narr) > 100:
        state['narration_log'] = narr[-100:]
    c.current_state = state
    _save_state(c)

    # Post to Discord
    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio

        async def _send_scene():
            from services.discord_bot import narration_embed
            discord_cfg = state.get('discord', {})
            tavern_id = discord_cfg.get('channels', {}).get('tavern')
            if tavern_id:
                ch = bot.get_channel(int(tavern_id))
                if ch:
                    await ch.send(embed=narration_embed(text, dm_name="Claude"))

        if _bot_loop and bot.is_ready():
            asyncio.run_coroutine_threadsafe(_send_scene(), _bot_loop)
    except Exception:
        pass

    _post_debug(c, f"[API] scene set: {text[:200]}")
    return jsonify(ok=True, text=text)


@api_bp.route('/npc/say', methods=['POST'])
@require_api_key
def api_npc_say():
    """
    Have an NPC speak.

    Body: {campaign_id, npc_name, text}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    npc_name = data.get('npc_name', '')
    text = data.get('text', '')

    if not all([cid, npc_name, text]):
        return jsonify(error="Required: campaign_id, npc_name, text"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    dialogue = f'**{npc_name}:** "{text}"'
    _log_action(c, npc_name, 'dialogue', dialogue)

    # Post to Discord
    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio
        import discord as _discord

        async def _send_npc():
            discord_cfg = (c.current_state or {}).get('discord', {})
            tavern_id = discord_cfg.get('channels', {}).get('tavern')
            if tavern_id:
                ch = bot.get_channel(int(tavern_id))
                if ch:
                    embed = _discord.Embed(
                        description=f'*"{text}"*',
                        color=0xC9A84C,
                    )
                    embed.set_author(name=npc_name)
                    await ch.send(embed=embed)

        if _bot_loop and bot.is_ready():
            asyncio.run_coroutine_threadsafe(_send_npc(), _bot_loop)
    except Exception:
        pass

    _post_debug(c, f"[API] NPC {npc_name} says: {text[:200]}")
    return jsonify(ok=True, npc=npc_name, text=text)


# ══════════════════════════════════════════════════════════════
# COMBAT
# ══════════════════════════════════════════════════════════════

@api_bp.route('/combat/start', methods=['POST'])
@require_api_key
def api_combat_start():
    """
    Start combat. Rolls initiative for all characters and NPCs.

    Body: {campaign_id}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    state['combat_active'] = True
    state['round'] = 1
    state['turn_index'] = 0

    # Roll initiative for everyone in the order
    order = state.get('initiative_order', [])
    for entry in order:
        roll, _, _ = DiceRoller.roll('1d20')
        entry['initiative'] = roll
    order.sort(key=lambda x: x.get('initiative', 0), reverse=True)
    state['initiative_order'] = order
    c.current_state = state
    _save_state(c)

    _log_action(c, 'System', 'combat', 'Combat started!')
    _post_debug(c, f"[API] combat started, {len(order)} combatants")

    return jsonify(ok=True, round=1, initiative_order=order)


@api_bp.route('/combat/next', methods=['POST'])
@require_api_key
def api_combat_next():
    """Advance to the next turn."""
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    order = state.get('initiative_order', [])
    if not order:
        return jsonify(error="No combatants in initiative"), 400

    idx = state.get('turn_index', 0) + 1
    if idx >= len(order):
        idx = 0
        state['round'] = state.get('round', 1) + 1

    state['turn_index'] = idx
    c.current_state = state
    _save_state(c)

    current = order[idx]
    _post_debug(c, f"[API] turn: {current.get('name')} (round {state['round']})")
    return jsonify(
        ok=True,
        round=state['round'],
        turn_index=idx,
        current_turn=current,
    )


@api_bp.route('/combat/end', methods=['POST'])
@require_api_key
def api_combat_end():
    """End combat."""
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    state['combat_active'] = False
    c.current_state = state
    _save_state(c)

    _log_action(c, 'System', 'combat', 'Combat ended.')
    _post_debug(c, "[API] combat ended")
    return jsonify(ok=True, message="Combat ended")


@api_bp.route('/damage', methods=['POST'])
@require_api_key
def api_damage():
    """
    Apply damage to a character or NPC.

    Body: {campaign_id, target, amount}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    target = data.get('target', '')
    amount = data.get('amount', 0)

    if not all([cid, target, amount]):
        return jsonify(error="Required: campaign_id, target, amount"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    # Try NPC first
    from services.engine import apply_damage_to_npc
    result = apply_damage_to_npc(c, target, int(amount))

    if 'error' in result:
        # Try as player character
        ch = Character.query.filter_by(campaign_id=cid, name=target).first()
        if ch:
            old_hp = ch.hp_current or 0
            ch.hp_current = max(0, old_hp - int(amount))
            db.session.commit()
            result = {
                'target': target,
                'old_hp': old_hp,
                'new_hp': ch.hp_current,
                'max_hp': ch.hp_max,
                'defeated': ch.hp_current <= 0,
            }
        else:
            return jsonify(error=result['error']), 404

    _log_action(c, 'API', 'damage', f"{target} takes {amount} damage (HP: {result['new_hp']}/{result['max_hp']})")
    _post_debug(c, f"[API] {target} takes {amount} dmg -> HP {result['new_hp']}/{result['max_hp']}")
    return jsonify(result=result)


@api_bp.route('/heal', methods=['POST'])
@require_api_key
def api_heal():
    """
    Heal a character or NPC.

    Body: {campaign_id, target, amount}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    target = data.get('target', '')
    amount = data.get('amount', 0)

    if not all([cid, target, amount]):
        return jsonify(error="Required: campaign_id, target, amount"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    # Try NPC
    state = c.current_state or {}
    healed = False
    for entry in state.get('initiative_order', []):
        if entry.get('is_npc') and entry.get('name', '').lower() == target.lower():
            old_hp = entry.get('npc_hp', 0)
            max_hp = entry.get('npc_hp_max', old_hp)
            entry['npc_hp'] = min(max_hp, old_hp + int(amount))
            c.current_state = state
            _save_state(c)
            result = {'target': target, 'old_hp': old_hp, 'new_hp': entry['npc_hp'], 'max_hp': max_hp}
            healed = True
            break

    if not healed:
        ch = Character.query.filter_by(campaign_id=cid, name=target).first()
        if ch:
            old_hp = ch.hp_current or 0
            ch.hp_current = min(ch.hp_max or 999, old_hp + int(amount))
            db.session.commit()
            result = {'target': target, 'old_hp': old_hp, 'new_hp': ch.hp_current, 'max_hp': ch.hp_max}
        else:
            return jsonify(error=f"Target '{target}' not found"), 404

    _log_action(c, 'API', 'heal', f"{target} healed {amount} HP (HP: {result['new_hp']}/{result['max_hp']})")
    _post_debug(c, f"[API] {target} healed {amount} -> HP {result['new_hp']}/{result['max_hp']}")
    return jsonify(result=result)


@api_bp.route('/condition', methods=['POST'])
@require_api_key
def api_condition():
    """
    Add or remove a condition.

    Body: {campaign_id, target, condition, action: "add"|"remove"}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    target = data.get('target', '')
    condition = data.get('condition', '')
    action = data.get('action', 'add')

    if not all([cid, target, condition]):
        return jsonify(error="Required: campaign_id, target, condition"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    conditions = state.setdefault('active_conditions', {})
    target_conditions = conditions.setdefault(target, [])

    if action == 'add':
        if condition not in target_conditions:
            target_conditions.append(condition)
    elif action == 'remove':
        target_conditions = [x for x in target_conditions if x.lower() != condition.lower()]
        conditions[target] = target_conditions

    c.current_state = state
    _save_state(c)

    _log_action(c, 'API', 'condition', f"{target}: {action} {condition}")
    _post_debug(c, f"[API] condition {action}: {target} -> {condition}")
    return jsonify(ok=True, target=target, conditions=target_conditions)


@api_bp.route('/loot', methods=['POST'])
@require_api_key
def api_loot():
    """
    Announce loot / give items.

    Body: {campaign_id, character_id (optional), text}
    If character_id given, adds to their equipment.
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    char_id = data.get('character_id')
    text = data.get('text', '')

    if not cid or not text:
        return jsonify(error="Required: campaign_id, text"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    result = {'text': text}

    if char_id:
        ch = Character.query.get(char_id)
        if ch:
            equip = ch.equipment or []
            equip.append(text)
            ch.equipment = equip
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(ch, 'equipment')
            db.session.commit()
            result['character'] = ch.name
            result['equipment'] = equip

    _log_action(c, 'API', 'loot', f"Loot: {text}")
    _post_debug(c, f"[API] loot: {text}")
    return jsonify(ok=True, result=result)


# ══════════════════════════════════════════════════════════════
# NPC MANAGEMENT
# ══════════════════════════════════════════════════════════════

@api_bp.route('/npc/add', methods=['POST'])
@require_api_key
def api_npc_add():
    """
    Add an NPC to the campaign's initiative order.

    Body: {campaign_id, name, hp, ac, initiative (optional)}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    name = data.get('name', '')
    hp = data.get('hp', 10)
    ac = data.get('ac', 10)
    initiative = data.get('initiative')

    if not cid or not name:
        return jsonify(error="Required: campaign_id, name"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    if initiative is None:
        roll, _, _ = DiceRoller.roll('1d20')
        initiative = roll

    state = c.current_state or {}
    order = state.setdefault('initiative_order', [])
    order.append({
        'name': name,
        'is_npc': True,
        'npc_hp': int(hp),
        'npc_hp_max': int(hp),
        'npc_ac': int(ac),
        'initiative': int(initiative),
    })
    order.sort(key=lambda x: x.get('initiative', 0), reverse=True)
    c.current_state = state
    _save_state(c)

    _log_action(c, 'API', 'npc', f"NPC added: {name} (HP:{hp} AC:{ac})")
    _post_debug(c, f"[API] NPC added: {name} HP:{hp} AC:{ac} Init:{initiative}")
    return jsonify(ok=True, npc={'name': name, 'hp': hp, 'ac': ac, 'initiative': initiative})


@api_bp.route('/npc/remove', methods=['POST'])
@require_api_key
def api_npc_remove():
    """
    Remove an NPC from initiative.

    Body: {campaign_id, name}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    name = data.get('name', '')

    if not cid or not name:
        return jsonify(error="Required: campaign_id, name"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    order = state.get('initiative_order', [])
    state['initiative_order'] = [x for x in order if x.get('name', '').lower() != name.lower()]
    c.current_state = state
    _save_state(c)

    _post_debug(c, f"[API] NPC removed: {name}")
    return jsonify(ok=True, removed=name)


# ══════════════════════════════════════════════════════════════
# DISCORD INTEGRATION
# ══════════════════════════════════════════════════════════════

@api_bp.route('/discord/send', methods=['POST'])
@require_api_key
def api_discord_send():
    """
    Post a message to a campaign's Discord channel.

    Body: {campaign_id, channel ("tavern"|"combat"|"quests"|"lore"|"debug"|"dm_screen"), text}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    channel_name = data.get('channel', 'tavern')
    text = data.get('text', '')

    if not cid or not text:
        return jsonify(error="Required: campaign_id, text"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    discord_cfg = state.get('discord', {})
    if not discord_cfg.get('enabled'):
        return jsonify(error="Discord not enabled for this campaign"), 400

    channel_id = discord_cfg.get('channels', {}).get(channel_name)
    if not channel_id:
        return jsonify(error=f"Channel '{channel_name}' not found"), 404

    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio

        async def _send():
            ch = bot.get_channel(int(channel_id))
            if ch:
                await ch.send(text[:2000])
                return True
            return False

        if _bot_loop and bot.is_ready():
            future = asyncio.run_coroutine_threadsafe(_send(), _bot_loop)
            result = future.result(timeout=5)
            return jsonify(ok=result, channel=channel_name)
        else:
            return jsonify(error="Discord bot not connected"), 503
    except Exception as e:
        return jsonify(error=str(e)), 500


@api_bp.route('/discord/embed', methods=['POST'])
@require_api_key
def api_discord_embed():
    """
    Post a rich embed to a campaign's Discord channel.

    Body: {campaign_id, channel, title, description, color (hex int), fields [{name, value, inline}]}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    channel_name = data.get('channel', 'tavern')
    title = data.get('title', '')
    description = data.get('description', '')
    color = data.get('color', 0xC9A84C)
    fields = data.get('fields', [])

    if not cid:
        return jsonify(error="Required: campaign_id"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    state = c.current_state or {}
    channel_id = state.get('discord', {}).get('channels', {}).get(channel_name)
    if not channel_id:
        return jsonify(error=f"Channel '{channel_name}' not found"), 404

    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio
        import discord as _discord

        async def _send():
            ch = bot.get_channel(int(channel_id))
            if ch:
                embed = _discord.Embed(title=title, description=description, color=color)
                for f in fields:
                    embed.add_field(
                        name=f.get('name', ''),
                        value=f.get('value', ''),
                        inline=f.get('inline', False)
                    )
                await ch.send(embed=embed)
                return True
            return False

        if _bot_loop and bot.is_ready():
            future = asyncio.run_coroutine_threadsafe(_send(), _bot_loop)
            result = future.result(timeout=5)
            return jsonify(ok=result, channel=channel_name)
        else:
            return jsonify(error="Discord bot not connected"), 503
    except Exception as e:
        return jsonify(error=str(e)), 500


@api_bp.route('/discord/status', methods=['GET'])
@require_api_key
def api_discord_status():
    """Get Discord bot status."""
    try:
        from services.discord_bot import bot, _bot_loop
        if not _bot_loop or not bot.is_ready():
            return jsonify(connected=False, reason="Bot not running or not ready")

        guilds = [{'name': g.name, 'id': str(g.id), 'member_count': g.member_count} for g in bot.guilds]
        return jsonify(
            connected=True,
            bot_user=str(bot.user),
            bot_id=str(bot.user.id),
            guilds=guilds,
            latency_ms=round(bot.latency * 1000, 1),
        )
    except Exception as e:
        return jsonify(connected=False, error=str(e))


# ══════════════════════════════════════════════════════════════
# DIAGNOSTICS
# ══════════════════════════════════════════════════════════════

@api_bp.route('/diagnostics', methods=['GET'])
@require_api_key
def api_diagnostics():
    """Full system diagnostics."""
    results = {}

    # Environment
    results['env'] = {
        'XAI_API_KEY': bool(os.environ.get('XAI_API_KEY')),
        'TWILIO_ACCOUNT_SID': bool(os.environ.get('TWILIO_ACCOUNT_SID')),
        'TWILIO_AUTH_TOKEN': bool(os.environ.get('TWILIO_AUTH_TOKEN')),
        'TWILIO_PHONE_NUMBER': os.environ.get('TWILIO_PHONE_NUMBER', ''),
        'DISCORD_BOT_TOKEN': bool(os.environ.get('DISCORD_BOT_TOKEN')),
        'DISCORD_CLIENT_ID': os.environ.get('DISCORD_CLIENT_ID', ''),
        'CLAUDE_API_KEY': bool(os.environ.get('CLAUDE_API_KEY')),
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'development'),
    }

    # Database
    try:
        user_count = User.query.count()
        char_count = Character.query.count()
        campaign_count = Campaign.query.count()
        active_campaigns = Campaign.query.filter_by(is_active=True).count()
        results['database'] = {
            'status': 'ok',
            'users': user_count,
            'characters': char_count,
            'campaigns': campaign_count,
            'active_campaigns': active_campaigns,
        }
    except Exception as e:
        results['database'] = {'status': 'error', 'error': str(e)}

    # Discord
    try:
        from services.discord_bot import bot, _bot_loop
        if _bot_loop and bot.is_ready():
            results['discord'] = {
                'status': 'connected',
                'bot_user': str(bot.user),
                'guilds': [g.name for g in bot.guilds],
                'latency_ms': round(bot.latency * 1000, 1),
            }
        else:
            results['discord'] = {'status': 'disconnected'}
    except Exception as e:
        results['discord'] = {'status': 'error', 'error': str(e)}

    # Grok API
    try:
        from services.ai_dm import _api_key
        results['grok'] = {
            'configured': bool(_api_key()),
        }
    except Exception as e:
        results['grok'] = {'status': 'error', 'error': str(e)}

    # Twilio
    try:
        sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        results['twilio'] = {
            'configured': bool(sid and os.environ.get('TWILIO_AUTH_TOKEN')),
            'phone': os.environ.get('TWILIO_PHONE_NUMBER', ''),
        }
    except Exception as e:
        results['twilio'] = {'status': 'error', 'error': str(e)}

    return jsonify(diagnostics=results)


@api_bp.route('/diagnostics/test/<test_name>', methods=['POST'])
@require_api_key
def api_diagnostics_test(test_name):
    """
    Run a specific diagnostic test.

    Tests: grok, twilio, engine, discord
    """
    if test_name == 'grok':
        try:
            from services.ai_dm import _call
            text, err = _call([
                {'role': 'system', 'content': 'Reply with exactly: OK'},
                {'role': 'user', 'content': 'Health check'},
            ], temperature=0, max_tokens=10)
            if err:
                return jsonify(test=test_name, status='fail', error=err)
            return jsonify(test=test_name, status='pass', response=text)
        except Exception as e:
            return jsonify(test=test_name, status='fail', error=str(e))

    elif test_name == 'engine':
        try:
            from services.engine import resolve_roll
            result = resolve_roll('1d20')
            return jsonify(test=test_name, status='pass', result=result)
        except Exception as e:
            return jsonify(test=test_name, status='fail', error=str(e))

    elif test_name == 'discord':
        try:
            from services.discord_bot import bot, _bot_loop
            if _bot_loop and bot.is_ready():
                return jsonify(test=test_name, status='pass',
                               bot=str(bot.user), guilds=[g.name for g in bot.guilds])
            return jsonify(test=test_name, status='fail', error='Bot not connected')
        except Exception as e:
            return jsonify(test=test_name, status='fail', error=str(e))

    else:
        return jsonify(error=f"Unknown test: {test_name}"), 404


# ══════════════════════════════════════════════════════════════
# LOG & HISTORY
# ══════════════════════════════════════════════════════════════

@api_bp.route('/log/<int:cid>', methods=['GET'])
@require_api_key
def api_log(cid):
    """
    Get recent action history for a campaign.

    Query params: count (default 30), type (optional: combat, narration, sms)
    """
    c, err = _get_campaign_or_404(cid)
    if err:
        return err

    count = int(request.args.get('count', 30))
    log_type = request.args.get('type', 'all')
    state = c.current_state or {}

    result = {}
    if log_type in ('all', 'combat'):
        result['combat_log'] = (state.get('combat_log') or [])[-count:]
    if log_type in ('all', 'narration'):
        result['narration_log'] = (state.get('narration_log') or [])[-count:]
    if log_type in ('all', 'sms'):
        result['sms_log'] = (state.get('sms_log') or [])[-count:]

    return jsonify(campaign_id=cid, logs=result)


# ══════════════════════════════════════════════════════════════
# PLAY AS CHARACTER (for external AI agents like Claude)
# ══════════════════════════════════════════════════════════════

@api_bp.route('/play', methods=['POST'])
@require_api_key
def api_play():
    """
    Play as a character — designed for external AI agents (e.g. Claude).

    Body: {campaign_id, character_id, message}
    The message is a natural-language action from the character's perspective.
    It goes through the AI DM pipeline just like a human player's action,
    and the result is posted to Discord.

    Returns the AI DM's response and updated character state.
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    char_id = data.get('character_id')
    message = data.get('message', '')

    if not all([cid, char_id, message]):
        return jsonify(error="Required: campaign_id, character_id, message"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    _post_debug(c, f"[PLAY] {ch.name}: {message}")

    # Process through the AI DM pipeline
    from services.ai_dm import process_player_sms
    try:
        response = process_player_sms(message, ch, c)
    except Exception as e:
        _post_debug(c, f"[PLAY] error: {e}")
        return jsonify(error=str(e)), 500

    # Log the action
    _log_action(c, ch.name, 'play', f"{ch.name}: {message} → {response[:200]}")

    # Post to Discord tavern channel
    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio
        import discord as _discord

        async def _send():
            state = c.current_state or {}
            discord_cfg = state.get('discord', {})
            tavern_id = discord_cfg.get('channels', {}).get('tavern')
            if not tavern_id:
                return

            channel = bot.get_channel(int(tavern_id))
            if not channel:
                return

            from services.discord_bot import CLASS_COLORS, DM_COLOR
            color = CLASS_COLORS.get(ch.class_name, DM_COLOR)

            em = _discord.Embed(
                description=(
                    f"🤖 **{ch.name}** *(via Claude)*: _{message}_\n\n"
                    f"{response}"
                ),
                color=color,
            )
            await channel.send(embed=em)

            # Post to dice-log if there's a mechanical result
            if response.startswith('['):
                dice_log_id = discord_cfg.get('channels', {}).get('dice_log')
                if dice_log_id:
                    dice_ch = bot.get_channel(int(dice_log_id))
                    if dice_ch:
                        roll_em = _discord.Embed(
                            description=f"🎲 **{ch.name}**: {response}",
                            color=color,
                        )
                        await dice_ch.send(embed=roll_em)

        if _bot_loop and bot.is_ready():
            asyncio.run_coroutine_threadsafe(_send(), _bot_loop)
    except Exception:
        pass

    # Refresh character state after action
    db.session.refresh(ch)

    _post_debug(c, f"[PLAY] {ch.name} response: {response[:200]}")
    return jsonify(
        character=_char_json(ch),
        message=message,
        response=response,
        campaign_state={
            'combat_active': (c.current_state or {}).get('combat_active', False),
            'round': (c.current_state or {}).get('round', 0),
            'initiative_order': (c.current_state or {}).get('initiative_order', []),
        },
    )


@api_bp.route('/play/context', methods=['GET'])
@require_api_key
def api_play_context():
    """
    Get the current game context for a character — everything an AI agent
    needs to decide what to do next.

    Query params: campaign_id, character_id
    Returns: character sheet, recent log, combat state, party info.
    """
    cid = request.args.get('campaign_id', type=int)
    char_id = request.args.get('character_id', type=int)

    if not cid or not char_id:
        return jsonify(error="Required query params: campaign_id, character_id"), 400

    c, err = _get_campaign_or_404(cid)
    if err:
        return err
    ch = Character.query.get(char_id)
    if not ch:
        return jsonify(error=f"Character {char_id} not found"), 404

    state = c.current_state or {}

    # Get party members
    party = []
    for pid in (c.players or []):
        pc = Character.query.filter_by(user_id=pid, campaign_id=c.id).first()
        if not pc:
            pc = Character.query.filter_by(user_id=pid).first()
        if pc:
            party.append({
                'name': pc.name,
                'class': pc.class_name,
                'level': pc.level,
                'hp': f"{pc.hp_current}/{pc.hp_max}",
                'is_you': pc.id == ch.id,
            })

    # Recent events
    combat_log = (state.get('combat_log') or [])[-15:]
    narration_log = (state.get('narration_log') or [])[-5:]

    return jsonify(
        character=_char_json(ch),
        campaign={
            'id': c.id,
            'name': c.name,
            'combat_active': state.get('combat_active', False),
            'round': state.get('round', 0),
            'turn_index': state.get('turn_index', 0),
            'initiative_order': state.get('initiative_order', []),
            'active_conditions': state.get('active_conditions', {}),
            'session_active': state.get('session_active', False),
        },
        party=party,
        recent_combat_log=combat_log,
        recent_narration=narration_log,
    )


@api_bp.route('/whisper', methods=['POST'])
@require_api_key
def api_whisper():
    """
    Send a private message to a player via Discord DM.

    Body: {campaign_id, username, text}
    """
    data = request.get_json(force=True)
    cid = data.get('campaign_id')
    username = data.get('username', '')
    text = data.get('text', '')

    if not all([cid, username, text]):
        return jsonify(error="Required: campaign_id, username, text"), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.discord_id:
        return jsonify(error=f"User '{username}' not found or has no Discord linked"), 404

    try:
        from services.discord_bot import bot, _bot_loop
        import asyncio

        async def _dm():
            discord_user = await bot.fetch_user(int(user.discord_id))
            if discord_user:
                await discord_user.send(f"**[DM Whisper]** {text}")
                return True
            return False

        if _bot_loop and bot.is_ready():
            future = asyncio.run_coroutine_threadsafe(_dm(), _bot_loop)
            result = future.result(timeout=5)
            _post_debug(Campaign.query.get(cid), f"[API] whisper to {username}: {text[:100]}")
            return jsonify(ok=result, to=username)
        else:
            return jsonify(error="Discord bot not connected"), 503
    except Exception as e:
        return jsonify(error=str(e)), 500
