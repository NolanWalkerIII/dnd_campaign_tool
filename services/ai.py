"""
xAI Grok API wrapper for DM narration features.

The XAI_API_KEY must be set in the .env file (never hard-coded).
If the key is missing or the request fails, functions return an error
string rather than raising so the UI can show a graceful message.
"""
import os
import time
from collections import deque
from datetime import datetime

import requests

XAI_API_URL = "https://api.x.ai/v1/chat/completions"
XAI_MODEL   = "grok-3-latest"
TIMEOUT     = 30  # seconds

# Characters that can be used to break out of prompt context or inject instructions
_PROMPT_STRIP = str.maketrans('', '', '<>{}\\`')
_MAX_USER_INPUT_LEN = 1000


def sanitize_for_prompt(text, max_len=_MAX_USER_INPUT_LEN):
    """
    Strip characters that could be used for prompt injection before embedding
    user-supplied strings in AI system/user messages.
    Removes < > { } \\ ` and truncates to max_len.
    """
    if not text:
        return ''
    return str(text).translate(_PROMPT_STRIP)[:max_len]

# In-memory ring buffer — last 500 API calls, resets on restart
_usage_log = deque(maxlen=500)


def get_usage_log():
    """Return a list of recent API call records (newest first)."""
    return list(reversed(_usage_log))


def _api_key():
    return os.environ.get("XAI_API_KEY", "")


def _call(messages, max_tokens=600):
    """
    Send a chat completion request to xAI Grok.
    Returns (text, error) — one of them will be None.
    """
    key = _api_key()
    if not key:
        return None, "XAI_API_KEY is not set. Add it to your .env file."

    t0 = time.time()
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
                "temperature": 0.8,
                "max_tokens": max_tokens,
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
        usage = data.get("usage", {})
        _usage_log.append({
            'ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0),
            'max_tokens': max_tokens,
            'latency': round(time.time() - t0, 2),
            'success': True,
            'error': None,
        })
        return text, None
    except requests.exceptions.Timeout:
        _usage_log.append({'ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                           'latency': round(time.time() - t0, 2), 'success': False,
                           'error': 'timeout', 'total_tokens': 0})
        return None, "xAI request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        _usage_log.append({'ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                           'latency': round(time.time() - t0, 2), 'success': False,
                           'error': f'http_{status}', 'total_tokens': 0})
        if status == 401:
            return None, "Invalid XAI_API_KEY. Check your .env file."
        return None, f"xAI API error ({status}). Please try again."
    except Exception as e:
        _usage_log.append({'ts': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                           'latency': round(time.time() - t0, 2), 'success': False,
                           'error': str(e)[:80], 'total_tokens': 0})
        return None, f"Unexpected error contacting xAI: {e}"


def generate_character(race, class_name, background, alignment,
                       name_hint='', prompts=None):
    """
    Generate a complete D&D 5e character concept using xAI Grok.

    Returns (result_dict, error). result_dict contains:
        name, backstory, personality_traits, ideals, bonds, flaws, appearance,
        ability_priorities (list of 6 ability score abbreviations, highest → lowest),
        suggested_skills (list of skill name strings)
    """
    import json as _json

    prompts = prompts or {}
    hint_line  = f'Name hint: "{name_hint}"' if name_hint else 'Generate a fitting name.'
    prompt_text = '\n'.join(
        f'- {v}' for v in prompts.values() if v and v.strip()
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative D&D 5e character generator. "
                "You MUST respond with ONLY a valid JSON object — no markdown code fences, "
                "no preamble, no explanation. The response must be pure JSON parseable directly.\n"
                "Required keys:\n"
                '  "name": string — a fitting D&D character name\n'
                '  "backstory": string — origin story, 2-3 paragraphs, grounded in D&D lore\n'
                '  "personality_traits": string — how they act day-to-day, 1-2 sentences\n'
                '  "ideals": string — the principle they live by, 1-2 sentences\n'
                '  "bonds": string — what ties them to the world, 1-2 sentences\n'
                '  "flaws": string — their weakness or blind spot, 1-2 sentences\n'
                '  "appearance": string — physical description, 2-3 sentences\n'
                '  "ability_priorities": array of exactly 6 strings from '
                '["STR","DEX","CON","INT","WIS","CHA"], ordered most-to-least important '
                'for this character — the standard array [15,14,13,12,10,8] is assigned in this order\n'
                '  "suggested_skills": array of 2-4 D&D 5e skill name strings fitting this character'
            ),
        },
        {
            "role": "user",
            "content": (
                f"Create a D&D 5e character:\n"
                f"Race: {race}\nClass: {class_name}\n"
                f"Background: {background}\nAlignment: {alignment}\n"
                f"{hint_line}\n"
                + (f"\nPlayer's concept notes:\n{prompt_text}\n" if prompt_text else "")
                + "\nRespond with ONLY the JSON object."
            ),
        },
    ]

    text, error = _call(messages, max_tokens=1400)
    if error:
        return None, error

    # Strip any markdown fences the model might wrap around the JSON
    text = text.strip()
    if text.startswith('```'):
        lines = text.split('\n')
        text = '\n'.join(lines[1:]).rstrip('`').strip()

    try:
        data = _json.loads(text)
    except _json.JSONDecodeError:
        return None, "AI returned an unexpected format. Please try again."

    # Validate and normalise ability_priorities
    valid_abs  = {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}
    priorities = [p.upper().strip() for p in data.get('ability_priorities', [])
                  if p.upper().strip() in valid_abs]
    seen = set()
    deduped = []
    for p in priorities:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    for ab in ['STR', 'CON', 'DEX', 'WIS', 'INT', 'CHA']:
        if ab not in seen:
            deduped.append(ab)
    priorities = deduped[:6]

    return {
        'name':               str(data.get('name', 'Unnamed Hero')).strip(),
        'backstory':          str(data.get('backstory', '')).strip(),
        'personality_traits': str(data.get('personality_traits', '')).strip(),
        'ideals':             str(data.get('ideals', '')).strip(),
        'bonds':              str(data.get('bonds', '')).strip(),
        'flaws':              str(data.get('flaws', '')).strip(),
        'appearance':         str(data.get('appearance', '')).strip(),
        'ability_priorities': priorities,
        'suggested_skills':   [str(s).strip() for s in data.get('suggested_skills', [])],
    }, None


def cleanup_narration(raw_text):
    """
    Polish the DM's raw narration text.
    Returns (cleaned_text, error).
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant for a Dungeons & Dragons campaign. "
                "Your job is to refine the Dungeon Master's narration: fix grammar and flow, "
                "improve atmosphere and word choice, and make it feel immersive — "
                "but keep the exact same meaning, tone, and content. "
                "Return only the refined narration text, no commentary."
            ),
        },
        {
            "role": "user",
            "content": f"Please clean up and refine this D&D narration:\n\n{raw_text}",
        },
    ]
    return _call(messages)


def summarize_chapter(chapter_title, chapter_notes, combat_log_entries=None):
    """
    Generate an AI summary for a completed chapter.
    chapter_title: string
    chapter_notes: string (DM's notes for the chapter)
    combat_log_entries: optional list of recent log entries for context
    Returns (summary_text, error).
    """
    context_parts = []
    if chapter_notes:
        context_parts.append(f"Chapter notes: {chapter_notes}")
    if combat_log_entries:
        recent = combat_log_entries[-10:]
        log_text = "\n".join(
            f"[{e.get('timestamp', '')}] {e.get('actor', '')}: {e.get('text', '')}"
            for e in recent
        )
        context_parts.append(f"Recent combat log:\n{log_text}")
    context = "\n\n".join(context_parts) if context_parts else "No additional context provided."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative Dungeon Master summarizing a completed chapter of a D&D 5e campaign. "
                "Write a vivid, atmospheric 2-4 sentence summary of what transpired, suitable to read "
                "aloud to players as a chapter recap. Use past tense, third-person perspective. "
                "Return only the summary text, no title or commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f'Summarize Chapter: "{chapter_title}"\n\n{context}'
            ),
        },
    ]
    return _call(messages)


def cleanup_background(raw_text, char_name, race, class_name):
    """Polish a player's custom background text. Returns (text, error)."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant helping a D&D 5e player refine their character's backstory. "
                "Fix grammar, improve flow and atmosphere, and make it feel vivid and immersive — "
                "but keep the exact same meaning, events, and character details. "
                "Return only the refined backstory text, no commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Character: {char_name}, {race} {class_name}\n\n"
                f"Please clean up and refine this backstory:\n\n{raw_text}"
            ),
        },
    ]
    return _call(messages)


def generate_background(char_name, race, class_name, background_preset, alignment):
    """Generate a custom backstory from character info. Returns (text, error)."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant helping a D&D 5e player create a compelling character backstory. "
                "Write an engaging, atmospheric 2-4 paragraph origin story. "
                "Make it specific and personal — include formative events, motivations, and a hint of what drives them to adventure. "
                "Return only the backstory text, no headers or commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Name: {char_name}\nRace: {race}\nClass: {class_name}\n"
                f"Background: {background_preset or 'unspecified'}\n"
                f"Alignment: {alignment or 'unspecified'}\n\n"
                "Write a compelling, original character backstory."
            ),
        },
    ]
    return _call(messages)


def generate_trait_field(field, custom_background, char_name, race, class_name):
    """
    Generate personality_traits, ideals, bonds, or flaws from the custom background.
    Returns (text, error).
    """
    prompts = {
        'personality_traits': (
            "personality traits",
            "Write 1-3 specific personality traits — quirks, mannerisms, or habits that define how this character acts day-to-day.",
        ),
        'ideals': (
            "ideals",
            "Write 1-2 ideals — the core beliefs or principles this character holds dear. Reflect their alignment.",
        ),
        'bonds': (
            "bonds",
            "Write 1-2 bonds — connections to people, places, or events that motivate and ground this character.",
        ),
        'flaws': (
            "flaws",
            "Write 1-2 flaws — weaknesses, vices, fears, or compulsions that create interesting complications.",
        ),
    }
    label, instruction = prompts.get(field, ("trait", "Write a character trait."))
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a creative writing assistant helping a D&D 5e player develop their character's {label}. "
                f"{instruction} "
                "Base your response on the character's backstory. Be specific and flavourful. "
                "Return only the trait text itself, no labels or commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Character: {char_name}, {race} {class_name}\n\n"
                f"Backstory:\n{custom_background}\n\n"
                f"Generate the character's {label}."
            ),
        },
    ]
    return _call(messages)


def generate_appearance(custom_background, physical_characteristics, char_name, race, class_name):
    """
    Generate an appearance description from physical characteristics + custom background.
    physical_characteristics: dict of filled fields.
    Returns (text, error).
    """
    phys_text = ", ".join(f"{k}: {v}" for k, v in physical_characteristics.items() if v)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant helping a D&D 5e player describe their character's appearance. "
                "Write a vivid, evocative 2-4 sentence description of how this character looks — their bearing, "
                "clothing style, distinguishing features, and the impression they make on others. "
                "Use the physical characteristics provided and let the backstory inform scars, posture, and tells. "
                "Return only the appearance description, no commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Character: {char_name}, {race} {class_name}\n"
                f"Physical characteristics: {phys_text}\n\n"
                f"Backstory:\n{custom_background}\n\n"
                "Describe this character's physical appearance."
            ),
        },
    ]
    return _call(messages)


def generate_narration(narration_log):
    """
    Generate a new narration entry based on the recent narration log.
    narration_log is a list of {'text': ..., 'timestamp': ...} dicts.
    Returns (generated_text, error).
    """
    if not narration_log:
        context = "The adventure is just beginning."
    else:
        # Use the last 5 entries as context
        recent = narration_log[-5:]
        context = "\n\n".join(
            f"[{e.get('timestamp', '')}] {e.get('text', '')}" for e in recent
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative Dungeon Master writing narration for a D&D 5e campaign. "
                "Based on the recent narration log provided, write a compelling continuation "
                "for the next scene. Keep it vivid, atmospheric, and 2-4 sentences long. "
                "Return only the narration text, no commentary or stage directions."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Here is the recent narration log:\n\n{context}\n\n"
                "Write the next scene narration to continue the story."
            ),
        },
    ]
    return _call(messages)


def cleanup_player_narration(raw_text, char_name, race, class_name, personality_traits=''):
    """
    Polish a player's in-character narration draft in their character's voice.
    Returns (cleaned_text, error).
    """
    trait_line = f"\nPersonality: {personality_traits}" if personality_traits else ""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant helping a D&D 5e player write in-character narration. "
                "Refine the player's text: fix grammar, improve flow and atmosphere, and make it feel vivid "
                "and true to their character — but keep the exact same meaning and events. "
                "Write in first person if the original is, third person if the original is. "
                "Return only the refined narration text, no commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Character: {char_name}, a {race} {class_name}{trait_line}\n\n"
                f"Please refine this in-character narration:\n\n{raw_text}"
            ),
        },
    ]
    return _call(messages)


def generate_player_narration(char_name, race, class_name, personality_traits='', recent_log=None):
    """
    Generate a short in-character action or dialogue for a player based on the current scene.
    Returns (text, error).
    """
    if recent_log:
        context_lines = [
            f"[{e.get('author', 'DM')}] {e.get('text', '')}"
            for e in recent_log[-5:]
            if e.get('type') != 'session_start'
        ]
        scene_context = "\n".join(context_lines) or "The adventure is just beginning."
    else:
        scene_context = "The adventure is just beginning."

    trait_line = f"\nPersonality traits: {personality_traits}" if personality_traits else ""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative writing assistant helping a D&D 5e player contribute in-character "
                "narration to a shared story. Write a short, vivid 1-3 sentence description of what "
                "their character does or says, consistent with their personality and the current scene. "
                "Write in third person (e.g. 'Aldric steps forward...'). "
                "Return only the narration text, no commentary."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Character: {char_name}, a {race} {class_name}{trait_line}\n\n"
                f"Recent scene:\n{scene_context}\n\n"
                "Generate a short in-character action or line of dialogue for this character."
            ),
        },
    ]
    return _call(messages)


def summarize_session(entries, session_name):
    """
    Generate an AI recap of a play session from its narration log entries.
    entries: list of narration_log dicts between session markers.
    session_name: string label (e.g. "Session 3").
    Returns (summary_text, error).
    """
    if not entries:
        return None, "No narration entries found for this session."

    log_text = "\n".join(
        f"[{e.get('author', 'DM')}] {e.get('text', '')}"
        for e in entries
        if e.get('type') != 'session_start'
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Dungeon Master writing a session recap for a D&D 5e campaign. "
                "Read the narration log and write a vivid, engaging 3-5 sentence summary of what transpired. "
                "Write in past tense, third-person. Capture key events, dramatic moments, and where "
                "the party now stands. Return only the recap text, no title or commentary."
            ),
        },
        {
            "role": "user",
            "content": f"Summarize {session_name} from this narration log:\n\n{log_text}",
        },
    ]
    return _call(messages, max_tokens=400)
