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
