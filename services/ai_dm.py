"""
AI Dungeon Master powered by xAI Grok.

Two-phase pipeline:
1. Interpret player's natural language → structured action JSON
2. Resolve mechanics via engine → narrate the result

Uses the same Grok API pattern as services/ai.py.
"""
import json
import os
import requests

from game_data import SKILLS
from services.engine import (
    get_character_summary,
    get_combat_state_summary,
    get_recent_log,
    resolve_skill_check,
    resolve_attack,
    resolve_roll,
    resolve_saving_throw,
    apply_damage_to_npc,
)

XAI_API_URL = "https://api.x.ai/v1/chat/completions"
XAI_MODEL = "grok-3-latest"
TIMEOUT = 15


def _api_key():
    return os.environ.get("XAI_API_KEY", "")


def _call(messages, temperature=0.7, max_tokens=400):
    key = _api_key()
    if not key:
        return None, "XAI_API_KEY is not set."

    try:
        resp = requests.post(
            XAI_API_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": XAI_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"].strip()
        return text, None
    except requests.exceptions.Timeout:
        return None, "AI DM request timed out."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        return None, f"AI DM API error ({status})."
    except Exception as e:
        return None, f"AI DM error: {e}"


SKILL_LIST = ", ".join(sorted(SKILLS.keys()))

INTERPRET_SYSTEM = f"""You are an AI Dungeon Master for D&D 5e played over SMS.
Given a player's message and game context, classify the action and return ONLY valid JSON.

Response format (no markdown, no explanation, ONLY the JSON object):
{{
  "action_type": "attack" | "skill_check" | "saving_throw" | "spell" | "roleplay" | "question",
  "params": {{}},
  "narration_context": "brief description of what's happening"
}}

Parameter rules by action_type:
- "attack": {{"target": "enemy name", "ability": "STR" or "DEX", "damage_dice": "1d8"}}
  Use STR for melee weapons, DEX for ranged/finesse. Infer from character equipment.
- "skill_check": {{"skill": "one of the valid skills"}}
  Valid skills: {SKILL_LIST}
  Examples: searching = Perception or Investigation, sneaking = Stealth, persuading = Persuasion
- "saving_throw": {{"ability": "STR"|"DEX"|"CON"|"INT"|"WIS"|"CHA"}}
- "spell": {{"spell_name": "spell name"}} — resolve as roleplay narration for now
- "roleplay": {{}} — no params, just narrate the player's action
- "question": {{}} — player asking about rules, their character, or game state

If unsure, default to "roleplay"."""


def interpret_action(player_message, character, campaign):
    """
    Ask Grok to interpret a player's natural language action.
    Returns (action_dict, error).
    """
    char_summary = get_character_summary(character)
    combat_summary = get_combat_state_summary(campaign)
    recent = get_recent_log(campaign)

    user_prompt = f"""PLAYER CHARACTER:
{char_summary}

GAME STATE:
{combat_summary}

RECENT EVENTS:
{recent}

The player says: "{player_message}"

Return ONLY valid JSON."""

    messages = [
        {"role": "system", "content": INTERPRET_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]

    text, error = _call(messages, temperature=0.3, max_tokens=200)
    if error:
        return None, error

    # Parse JSON — strip markdown fences if present
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = '\n'.join(cleaned.split('\n')[1:])
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    try:
        action = json.loads(cleaned)
        if 'action_type' not in action:
            action['action_type'] = 'roleplay'
        if 'params' not in action:
            action['params'] = {}
        return action, None
    except json.JSONDecodeError:
        # Fallback to roleplay if JSON parsing fails
        return {
            'action_type': 'roleplay',
            'params': {},
            'narration_context': player_message,
        }, None


def narrate_result(action_type, params, engine_result, character, campaign):
    """
    Given mechanical results, generate atmospheric SMS-length narration.
    Returns (narration_text, error).
    """
    char_name = character.name
    combat_summary = get_combat_state_summary(campaign)

    mechanic_text = engine_result.get('text', '')

    user_prompt = f"""Character: {char_name}
Action: {action_type}
Mechanic result: {mechanic_text}
Game state: {combat_summary}
Context: {params.get('narration_context', '')}

Write a brief, atmospheric D&D narration of this result. MUST be under 280 characters.
Include the mechanical result naturally (e.g., the roll total).
Return ONLY the narration text."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a vivid D&D narrator. Write concise, atmospheric narration for SMS. "
                "Under 280 characters. No meta-commentary. Just the narration."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]

    text, error = _call(messages, temperature=0.8, max_tokens=150)
    if error:
        # Fallback: return just the mechanical text
        return mechanic_text, None
    return text, None


def answer_question(player_message, character, campaign):
    """Answer a rules or game-state question."""
    char_summary = get_character_summary(character)
    combat_summary = get_combat_state_summary(campaign)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful D&D 5e rules expert responding via SMS. "
                "Answer concisely (under 300 chars). Use the character and game context provided."
            ),
        },
        {
            "role": "user",
            "content": f"Character: {char_summary}\nGame: {combat_summary}\n\nQuestion: {player_message}",
        },
    ]

    text, error = _call(messages, temperature=0.5, max_tokens=150)
    if error:
        return f"Sorry, I couldn't process that: {error}"
    return text


def process_player_sms(player_message, character, campaign):
    """
    Full pipeline: interpret → resolve → narrate → return SMS text.
    Also logs the action to the campaign's SMS log.
    """
    from models import db
    from sqlalchemy.orm.attributes import flag_modified

    # 1. Interpret the player's intent
    action, error = interpret_action(player_message, character, campaign)
    if error:
        return f"[AI DM Error] {error}"

    action_type = action['action_type']
    params = action.get('params', {})
    narration_context = action.get('narration_context', '')

    # 2. Resolve mechanics
    engine_result = {}

    if action_type == 'attack':
        engine_result = resolve_attack(
            character, campaign,
            target_name=params.get('target', 'target'),
            ability=params.get('ability', 'STR'),
            damage_dice=params.get('damage_dice'),
            target_ac=params.get('target_ac'),
        )
        # Apply damage to NPC if in combat and hit
        if engine_result.get('damage_total') and engine_result.get('hit') is not False:
            npc_result = apply_damage_to_npc(
                campaign, params.get('target', ''), engine_result['damage_total']
            )
            if not npc_result.get('error'):
                engine_result['text'] += f' ({npc_result["npc_name"]} HP: {npc_result["new_hp"]}/{npc_result["max_hp"]})'
                if npc_result['defeated']:
                    engine_result['text'] += ' DEFEATED!'

    elif action_type == 'skill_check':
        skill = params.get('skill', '')
        engine_result = resolve_skill_check(character, campaign, skill)

    elif action_type == 'saving_throw':
        engine_result = resolve_saving_throw(character, params.get('ability', 'CON'))

    elif action_type == 'question':
        response = answer_question(player_message, character, campaign)
        _log_sms(campaign, character.name, player_message, response)
        return response

    elif action_type in ('roleplay', 'spell'):
        engine_result = {'text': ''}
        params['narration_context'] = narration_context

    # 3. Check for engine errors
    if engine_result.get('error'):
        return f"[Error] {engine_result['error']}"

    # 4. Narrate the result
    narration, _ = narrate_result(action_type, params, engine_result, character, campaign)

    # 5. Compose SMS response
    mechanic_text = engine_result.get('text', '')
    if mechanic_text:
        response = f"[{mechanic_text}] {narration}"
    else:
        response = narration

    # 6. Log to campaign state and combat log
    _log_sms(campaign, character.name, player_message, response)

    if mechanic_text:
        from services.engine import mod_str
        state = campaign.current_state or {}
        log = state.get('combat_log', [])
        from datetime import datetime
        log.append({
            'actor': character.name,
            'text': mechanic_text,
            'timestamp': datetime.now().strftime('%H:%M'),
            'type': action_type,
        })
        state['combat_log'] = log
        campaign.current_state = state
        flag_modified(campaign, 'current_state')
        db.session.commit()

    return response


def generate_agent_response(character, campaign, acting_char_name, player_msg, dm_response):
    """
    Generate an AI agent response for an absent player's character.
    Uses the character's past SMS history to mimic their play style.
    Returns a short action string (what the agent character does).
    """
    char_summary = get_character_summary(character)
    combat_summary = get_combat_state_summary(campaign)

    # Gather past SMS behavior for this character
    state = campaign.current_state or {}
    sms_log = state.get('sms_log', [])
    past_actions = []
    for entry in sms_log:
        if entry.get('player') == character.name and entry.get('player') != 'AI DM':
            past_actions.append(entry.get('message', ''))
    past_actions = past_actions[-10:]  # Last 10 actions

    past_context = '\n'.join(f'- {a}' for a in past_actions) if past_actions else 'No past actions yet.'

    messages = [
        {
            "role": "system",
            "content": (
                f"You are playing as {character.name} in a D&D game over SMS. "
                f"Another player just acted and the DM responded. Now it's your turn to react.\n\n"
                f"CHARACTER: {char_summary}\n\n"
                f"PLAY STYLE (based on past actions):\n{past_context}\n\n"
                f"Stay in character. Write a SHORT action (under 80 chars) that {character.name} "
                f"would do in response. Just the action, nothing else. "
                f"Examples: 'I check the corridor for traps', 'I ready my sword and watch the door', "
                f"'I cast detect magic on the artifact'"
            ),
        },
        {
            "role": "user",
            "content": (
                f"GAME STATE: {combat_summary}\n\n"
                f"{acting_char_name} said: \"{player_msg}\"\n"
                f"DM responded: \"{dm_response}\"\n\n"
                f"What does {character.name} do?"
            ),
        },
    ]

    text, error = _call(messages, temperature=0.8, max_tokens=100)
    if error:
        return None
    return text.strip()[:160]


def _log_sms(campaign, char_name, player_msg, dm_response):
    """Append to the SMS activity log in campaign state."""
    from models import db
    from sqlalchemy.orm.attributes import flag_modified
    from datetime import datetime

    state = campaign.current_state or {}
    sms_log = state.get('sms_log', [])

    now = datetime.now().strftime('%H:%M')
    sms_log.append({
        'timestamp': now,
        'player': char_name,
        'message': player_msg,
    })
    sms_log.append({
        'timestamp': now,
        'player': 'AI DM',
        'message': dm_response,
    })

    # Keep last 50 entries
    state['sms_log'] = sms_log[-50:]
    campaign.current_state = state
    flag_modified(campaign, 'current_state')
    db.session.commit()
