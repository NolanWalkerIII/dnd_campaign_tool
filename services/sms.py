"""
Twilio SMS wrapper for sending and receiving text messages.

Environment variables:
  TWILIO_ACCOUNT_SID  — Twilio account SID
  TWILIO_AUTH_TOKEN   — Twilio auth token
  TWILIO_PHONE_NUMBER — Your Twilio phone number (e.g., +15551234567)
"""
import os


def _get_client():
    from twilio.rest import Client
    sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    if not sid or not token:
        return None
    return Client(sid, token)


def send_sms(to_number, body):
    """
    Send an SMS via Twilio.
    Returns (message_sid, error).
    """
    client = _get_client()
    if not client:
        return None, "Twilio credentials not configured."

    from_number = os.environ.get('TWILIO_PHONE_NUMBER', '')
    if not from_number:
        return None, "TWILIO_PHONE_NUMBER not set."

    try:
        # Truncate to Twilio's max (1600 chars)
        body = body[:1600]
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number,
        )
        return message.sid, None
    except Exception as e:
        return None, f"SMS send error: {e}"


def validate_webhook(request):
    """
    Validate that an incoming request is from Twilio.
    Returns True if valid, False otherwise.
    In development (no auth token), always returns True.
    """
    token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    if not token:
        # Dev mode: skip validation
        return True

    try:
        from twilio.request_validator import RequestValidator
        validator = RequestValidator(token)
        # Behind a reverse proxy, request.url may be http:// but Twilio signed https://
        url = request.url
        if request.headers.get('X-Forwarded-Proto') == 'https':
            url = url.replace('http://', 'https://', 1)
        post_vars = request.form.to_dict()
        signature = request.headers.get('X-Twilio-Signature', '')
        return validator.validate(url, post_vars, signature)
    except Exception:
        return False


def parse_incoming(request):
    """
    Extract the sender's phone number and message body from a Twilio webhook.
    Returns (from_number, body).
    """
    from_number = request.form.get('From', '').strip()
    body = request.form.get('Body', '').strip()
    return from_number, body
