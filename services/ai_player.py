"""
AI Player service — generates in-character actions for AI-controlled characters.

Persona levels shape how the AI "plays":
  novice       — simple, hesitant, often forgets mechanics
  intermediate — competent, uses backstory, engages with story
  experienced  — tactical, distinct voice, creative solutions
"""
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
