"""
xAI Grok API wrapper for DM narration features.

The XAI_API_KEY must be set in the .env file (never hard-coded).
If the key is missing or the request fails, functions return an error
string rather than raising so the UI can show a graceful message.
"""
import os
import requests

XAI_API_URL = "https://api.x.ai/v1/chat/completions"
XAI_MODEL   = "grok-3-latest"
TIMEOUT     = 30  # seconds


def _api_key():
    return os.environ.get("XAI_API_KEY", "")


def _call(messages):
    """
    Send a chat completion request to xAI Grok.
    Returns (text, error) — one of them will be None.
    """
    key = _api_key()
    if not key:
        return None, "XAI_API_KEY is not set. Add it to your .env file."

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
                "max_tokens": 600,
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"].strip()
        return text, None
    except requests.exceptions.Timeout:
        return None, "xAI request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        if status == 401:
            return None, "Invalid XAI_API_KEY. Check your .env file."
        return None, f"xAI API error ({status}). Please try again."
    except Exception as e:
        return None, f"Unexpected error contacting xAI: {e}"


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
