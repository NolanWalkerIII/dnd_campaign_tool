"""
Pure-function game engine for SMS AI DM.

Extracts game logic from app.py route handlers into functions
that take model objects and return result dicts — no Flask
request/session/flash dependencies.
"""
import re
from models import DiceRoller
from game_data import SKILLS, CLASSES, ABILITY_SCORES


def ability_modifier(score):
    return (score - 10) // 2


def mod_str(m):
    return f'+{m}' if m >= 0 else str(m)


def get_combatant_conditions(state, key):
    return state.get('active_conditions', {}).get(str(key), [])


def char_attack_bonus(char, ability='STR'):
    score = (char.ability_scores or {}).get(ability, 10)
    return char.proficiency_bonus + ability_modifier(score)


def resolve_skill_check(character, campaign, skill_name):
    """
    Resolve a skill check for a character.
    Returns dict: {skill, ability, base_mod, prof_bonus, total_mod, roll, rolls, total, text}
    """
    if skill_name not in SKILLS:
        return {'error': f'Invalid skill: {skill_name}'}

    ab = SKILLS[skill_name]
    base = ability_modifier((character.ability_scores or {}).get(ab, 10))
    prof = character.proficiency_bonus if skill_name in (character.skills or []) else 0
    total_mod = base + prof

    roll, rolls, _ = DiceRoller.roll('1d20', modifier=total_mod)
    prof_tag = ' (prof)' if prof else ''

    text = f'{skill_name}{prof_tag}: d20({rolls[0]}){mod_str(total_mod)} = {roll}'

    return {
        'skill': skill_name,
        'ability': ab,
        'base_mod': base,
        'prof_bonus': prof,
        'total_mod': total_mod,
        'roll': roll,
        'rolls': rolls,
        'total': roll,
        'text': text,
    }


def resolve_attack(character, campaign, target_name='target', ability='STR',
                   damage_dice=None, target_ac=None):
    """
    Resolve an attack roll for a character.
    Returns dict with attack and optional damage results.
    """
    if ability not in ABILITY_SCORES:
        ability = 'STR'

    state = campaign.current_state or {}
    conds = get_combatant_conditions(state, character.id)
    has_disadvantage = 'Poisoned' in conds or 'Restrained' in conds
    has_advantage = 'Invisible' in conds

    atk_bonus = char_attack_bonus(character, ability)
    atk_total, rolls, is_crit = DiceRoller.roll(
        '1d20', modifier=atk_bonus,
        advantage=has_advantage, disadvantage=has_disadvantage
    )

    adv_tag = ' (adv)' if has_advantage else (' (disadv)' if has_disadvantage else '')
    crit_tag = ' CRIT!' if is_crit else ''

    hit = None
    hit_tag = ''
    if target_ac is not None:
        hit = atk_total >= target_ac or is_crit
        hit_tag = ' HIT!' if hit else ' MISS!'

    result = {
        'target': target_name,
        'ability': ability,
        'atk_total': atk_total,
        'atk_rolls': rolls,
        'atk_bonus': atk_bonus,
        'is_crit': is_crit,
        'hit': hit,
        'has_advantage': has_advantage,
        'has_disadvantage': has_disadvantage,
        'text': f'Attack vs {target_name}{adv_tag}: d20({rolls[0]}){mod_str(atk_bonus)} = {atk_total}{hit_tag}{crit_tag}',
    }

    # Damage roll if applicable
    if damage_dice and (hit is True or hit is None or is_crit):
        try:
            dice_str = damage_dice
            if is_crit:
                m = re.match(r'^(\d+)d(\d+)([+-]\d+)?$', damage_dice.lower().strip())
                if m:
                    dice_str = f'{int(m.group(1))*2}d{m.group(2)}'
                    if m.group(3):
                        dice_str += m.group(3)

            ability_score = (character.ability_scores or {}).get(ability, 10)
            dmg_mod = ability_modifier(ability_score)
            total_dmg, label, dmg_rolls, _, _ = DiceRoller.parse_and_roll(dice_str)

            if not re.search(r'[+-]\d+$', damage_dice.lower().strip()):
                total_dmg += dmg_mod
                label = f'{damage_dice}{mod_str(dmg_mod)}'

            crit_label = ' (crit x2)' if is_crit else ''
            result['damage_total'] = total_dmg
            result['damage_rolls'] = dmg_rolls
            result['damage_label'] = label
            result['text'] += f', {total_dmg} dmg{crit_label}'
        except ValueError:
            result['damage_error'] = 'Invalid damage dice'

    return result


def resolve_roll(dice_str):
    """
    Simple dice roll.
    Returns dict: {total, label, rolls, modifier, is_crit, text}
    """
    try:
        total, label, rolls, mod, is_crit = DiceRoller.parse_and_roll(dice_str)
        crit_tag = ' CRIT!' if is_crit else ''
        return {
            'total': total,
            'label': label,
            'rolls': rolls,
            'modifier': mod,
            'is_crit': is_crit,
            'text': f'{label}: [{", ".join(str(r) for r in rolls)}] = {total}{crit_tag}',
        }
    except ValueError as e:
        return {'error': str(e)}


def resolve_saving_throw(character, ability):
    """
    Resolve a saving throw.
    Returns dict: {ability, modifier, roll, rolls, total, text}
    """
    if ability not in ABILITY_SCORES:
        return {'error': f'Invalid ability: {ability}'}

    score = (character.ability_scores or {}).get(ability, 10)
    mod = ability_modifier(score)
    total, rolls, _ = DiceRoller.roll('1d20', modifier=mod)

    return {
        'ability': ability,
        'modifier': mod,
        'roll': total,
        'rolls': rolls,
        'total': total,
        'text': f'{ability} save: d20({rolls[0]}){mod_str(mod)} = {total}',
    }


def get_character_summary(character):
    """One-line character summary for AI context."""
    scores = character.ability_scores or {}
    score_str = ' '.join(f'{a}:{scores.get(a, 10)}' for a in ABILITY_SCORES)
    spells_data = character.spells or {}
    known = spells_data.get('known', [])
    spells_str = f', Spells: {", ".join(known)}' if known else ''
    equip = character.equipment or []
    equip_str = f', Gear: {", ".join(equip[:5])}' if equip else ''

    return (
        f'{character.name}, Lv{character.level} {character.race} {character.class_name}, '
        f'HP {character.hp_current}/{character.hp_max}, AC {character.ac}, '
        f'{score_str}{spells_str}{equip_str}'
    )


def get_combat_state_summary(campaign):
    """Summary of combat state for AI context."""
    state = campaign.current_state or {}
    if not state.get('combat_active'):
        return 'Not in combat. Exploration mode.'

    order = state.get('initiative_order', [])
    turn_idx = state.get('turn_index', 0)
    round_num = state.get('round', 1)

    lines = [f'COMBAT — Round {round_num}']
    for i, entry in enumerate(order):
        marker = ' >> ' if i == turn_idx else '    '
        hp_str = ''
        if entry.get('is_npc') and entry.get('npc_hp') is not None:
            hp_str = f' (HP {entry["npc_hp"]}/{entry["npc_hp_max"]}, AC {entry.get("npc_ac", "?")})'
        conditions = get_combatant_conditions(state, entry.get('char_id') or entry.get('name', ''))
        cond_str = f' [{", ".join(conditions)}]' if conditions else ''
        lines.append(f'{marker}{entry["name"]} (Init {entry["initiative"]}){hp_str}{cond_str}')

    return '\n'.join(lines)


def get_recent_log(campaign, count=5):
    """Get recent narration and combat log entries as text."""
    state = campaign.current_state or {}
    entries = []

    narration = state.get('narration_log', [])
    for e in narration[-count:]:
        entries.append(f'[Narration] {e.get("text", "")}')

    combat = state.get('combat_log', [])
    for e in combat[-count:]:
        entries.append(f'[{e.get("type", "action")}] {e.get("actor", "")}: {e.get("text", "")}')

    return '\n'.join(entries[-count:]) if entries else 'The adventure is just beginning.'


def apply_damage_to_npc(campaign, npc_name, damage):
    """
    Find NPC in initiative order and reduce HP.
    Returns dict: {npc_name, old_hp, new_hp, max_hp, defeated}
    """
    state = campaign.current_state or {}
    order = state.get('initiative_order', [])

    for entry in order:
        if entry.get('is_npc') and entry['name'].lower() == npc_name.lower():
            old_hp = entry.get('npc_hp', 0)
            new_hp = max(0, old_hp - damage)
            entry['npc_hp'] = new_hp
            campaign.current_state = state
            return {
                'npc_name': entry['name'],
                'old_hp': old_hp,
                'new_hp': new_hp,
                'max_hp': entry.get('npc_hp_max', old_hp),
                'defeated': new_hp <= 0,
            }

    return {'error': f'NPC "{npc_name}" not found in combat.'}
