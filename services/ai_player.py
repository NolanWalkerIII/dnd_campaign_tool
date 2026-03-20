"""
AI Player service — generates in-character actions for AI-controlled characters.

Persona levels shape how the AI "plays":
  novice       — simple, hesitant, often forgets mechanics
  intermediate — competent, uses backstory, engages with story
  experienced  — tactical, distinct voice, creative solutions
"""
import json
import re
from services.ai import _call

PERSONA_PROMPTS = {
    'novice': (
        "You are roleplaying as a first-time tabletop RPG player controlling {name}. "
        "Speak simply and directly as your character. Ask the DM clarifying questions when unsure. "
        "Sometimes forget to use skills or special abilities. Focus on obvious actions rather than "
        "creative solutions. Keep your response to 1–3 sentences in first person."
    ),
    'intermediate': (
        "You are roleplaying as a player with some tabletop RPG experience controlling {name}. "
        "Use your character's backstory occasionally to inform decisions. "
        "Use skills and abilities when clearly relevant. Engage with NPCs and plot hooks. "
        "Keep your response to 1–3 sentences in first person."
    ),
    'experienced': (
        "You are roleplaying as a veteran tabletop RPG player controlling {name}. "
        "Your character has a distinct voice and references past events. "
        "Make mechanically efficient choices, look for creative solutions, ask probing questions "
        "of NPCs, and use all available tools. Keep your response to 1–3 sentences in first person."
    ),
}


def generate_player_action(character, campaign, persona_level):
    """
    Generate an in-character action for an AI-controlled character.
    Returns (action_text, error) — same pattern as other ai.py functions.
    """
    bg = (character.spells or {}).get('background_details', {})
    state = campaign.current_state or {}

    # Build scene context from recent narration log (last 5 entries)
    narration_log = state.get('narration_log', [])
    recent = narration_log[-5:] if narration_log else []
    if recent:
        scene = '\n'.join(e.get('text', '') for e in recent)
    else:
        scene = 'The adventure is just beginning.'

    # Character context
    char_ctx = (
        f"Character: {character.name}, "
        f"Level {character.level} {character.race} {character.class_name}\n"
        f"Background: {character.background or 'Unknown'}\n"
    )
    if bg.get('custom_background'):
        char_ctx += f"Backstory: {bg['custom_background'][:400]}\n"
    if bg.get('personality_traits'):
        char_ctx += f"Personality: {bg['personality_traits']}\n"
    if bg.get('ideals'):
        char_ctx += f"Ideals: {bg['ideals']}\n"
    if bg.get('bonds'):
        char_ctx += f"Bonds: {bg['bonds']}\n"
    if bg.get('flaws'):
        char_ctx += f"Flaws: {bg['flaws']}\n"

    level = persona_level if persona_level in PERSONA_PROMPTS else 'intermediate'
    system = PERSONA_PROMPTS[level].format(name=character.name)

    user_msg = (
        f"{char_ctx}\n"
        f"Current scene:\n{scene}\n\n"
        f"What does {character.name} do or say next? "
        f"Respond in first person as the character."
    )

    return _call(
        [{'role': 'system', 'content': system},
         {'role': 'user', 'content': user_msg}],
        max_tokens=300
    )


_COMBAT_PERSONA = {
    'novice': (
        "You are a first-time RPG player controlling {name} in combat. "
        "Choose a simple, obvious action — usually just attack the nearest enemy. "
        "You may forget bonus actions or special abilities. "
        "Return ONLY valid JSON (no markdown fences) with exactly these keys: "
        "action_type (one of: attack, spell, dash, help), "
        "target (name of the target or null), "
        "weapon_or_spell (weapon or spell name, or null), "
        "bonus_action (brief description or null), "
        "reasoning (one sentence)."
    ),
    'intermediate': (
        "You are an experienced RPG player controlling {name} in combat. "
        "Pick a tactically reasonable action — prioritize low-HP or dangerous enemies. "
        "Use bonus actions when available; conserve spell slots unless necessary. "
        "Return ONLY valid JSON (no markdown fences) with exactly these keys: "
        "action_type (one of: attack, spell, dash, help), "
        "target (name of the target or null), "
        "weapon_or_spell (weapon or spell name, or null), "
        "bonus_action (brief description or null), "
        "reasoning (one sentence)."
    ),
    'experienced': (
        "You are a veteran RPG player controlling {name} in combat. "
        "Make the most tactically efficient decision: focus-fire low-HP targets, "
        "maximise action economy, coordinate with allies, and exploit every advantage. "
        "Return ONLY valid JSON (no markdown fences) with exactly these keys: "
        "action_type (one of: attack, spell, dash, help), "
        "target (name of the target or null), "
        "weapon_or_spell (weapon or spell name, or null), "
        "bonus_action (brief description or null), "
        "reasoning (one sentence)."
    ),
}


def generate_combat_decision(character, campaign, persona_level):
    """
    Generate a structured combat decision for an AI-controlled character.
    Returns (decision_dict, error).
    decision_dict keys: action_type, target, weapon_or_spell, bonus_action, reasoning
    """
    state = campaign.current_state or {}
    order = state.get('initiative_order', [])
    combat_log = state.get('combat_log', [])
    conditions_map = state.get('active_conditions', {})

    # Build combatant list for context
    from models import Character as _Char
    combatant_lines = []
    for entry in order:
        if entry.get('is_npc'):
            combatant_lines.append(
                f"  NPC {entry['name']} "
                f"(HP: {entry['npc_hp']}/{entry['npc_hp_max']}, AC: {entry['npc_ac']})"
            )
        else:
            c = _Char.query.get(entry.get('char_id'))
            if c:
                combatant_lines.append(
                    f"  PC {c.name} (HP: {c.hp_current}/{c.hp_max}, AC: {c.ac})"
                )
    combatants_text = '\n'.join(combatant_lines) or '  No combatants visible.'

    # Recent combat log (last 6 entries)
    recent_log = combat_log[-6:] if combat_log else []
    log_text = '\n'.join(
        f"  {e.get('actor', '?')}: {e.get('text', '')}" for e in recent_log
    ) or '  (combat just started)'

    # Character state
    extra = character.spells or {}
    slots = extra.get('slots', {})
    slot_summary = ', '.join(f"L{k}:{v}" for k, v in slots.items() if v > 0) or 'none'
    cond_key = f'char_{character.id}'
    conditions = conditions_map.get(cond_key, [])
    cond_text = ', '.join(conditions) or 'none'

    char_ctx = (
        f"{character.name} — Lv{character.level} {character.race} {character.class_name}\n"
        f"HP: {character.hp_current}/{character.hp_max}  AC: {character.ac}  "
        f"Prof: +{character.proficiency_bonus}\n"
        f"Conditions: {cond_text}\n"
        f"Spell slots remaining: {slot_summary}\n"
        f"Equipment: {', '.join((character.equipment or [])[:6]) or 'none'}"
    )

    level = persona_level if persona_level in _COMBAT_PERSONA else 'intermediate'
    system = _COMBAT_PERSONA[level].format(name=character.name)

    user_msg = (
        f"Your character:\n{char_ctx}\n\n"
        f"All combatants:\n{combatants_text}\n\n"
        f"Recent combat log:\n{log_text}\n\n"
        f"It is {character.name}'s turn. Decide their action."
    )

    text, error = _call(
        [{'role': 'system', 'content': system},
         {'role': 'user', 'content': user_msg}],
        max_tokens=400
    )
    if error:
        return None, error

    # Strip markdown fences if present and parse JSON
    clean = re.sub(r'^```(?:json)?\s*', '', text.strip())
    clean = re.sub(r'\s*```$', '', clean)
    try:
        decision = json.loads(clean)
        return decision, None
    except Exception:
        # Fallback: wrap raw text so the UI still has something to show
        return {
            'action_type': 'attack',
            'target': None,
            'weapon_or_spell': None,
            'bonus_action': None,
            'reasoning': text,
        }, None
