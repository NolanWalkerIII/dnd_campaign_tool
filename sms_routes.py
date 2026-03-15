"""
SMS routes — Flask Blueprint for Twilio webhook, phone verification, and agent mode.
"""
import os
from flask import Blueprint, request, session, flash, redirect, url_for
from models import db, User, Character, Campaign
from sqlalchemy.orm.attributes import flag_modified

sms_bp = Blueprint('sms', __name__, url_prefix='/sms')


def _normalize_phone(phone):
    """Normalize a phone number to +1XXXXXXXXXX format."""
    if phone.startswith('+'):
        digits = phone[1:].replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        return '+' + digits
    digits = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if digits.startswith('1') and len(digits) == 11:
        return '+' + digits
    return '+1' + digits


# ── WEBHOOK ──────────────────────────────────────────────────

@sms_bp.route('/webhook', methods=['POST'])
def sms_webhook():
    """
    Twilio hits this endpoint when a player texts in.
    Handles two flows:
    1. Verification: player texts back the join code to confirm their phone
    2. Gameplay: player texts actions to the AI DM
    """
    from services.sms import validate_webhook, parse_incoming
    from services.ai_dm import process_player_sms

    if not validate_webhook(request):
        return '<Response><Message>Unauthorized.</Message></Response>', 403, {'Content-Type': 'text/xml'}

    from_number, body = parse_incoming(request)
    if not from_number or not body:
        return _twiml('Please send a message to play.')

    body_stripped = body.strip().upper()

    # ── Check for pending verification ──
    # Look through all campaigns for a pending verification matching this phone
    campaigns = Campaign.query.filter(Campaign.is_active == True).all()
    for c in campaigns:
        state = c.current_state or {}
        pending = state.get('pending_verifications', {})
        if from_number in pending:
            expected_code = pending[from_number]['join_code'].upper()
            user_id = pending[from_number]['user_id']

            if body_stripped == expected_code:
                # Verification successful — link the phone
                target_user = User.query.get(user_id)
                if target_user:
                    target_user.phone_number = from_number
                    # Remove from pending
                    del pending[from_number]
                    state['pending_verifications'] = pending
                    c.current_state = state
                    flag_modified(c, 'current_state')
                    db.session.commit()

                    # Send welcome message
                    _send_welcome_sms(from_number, target_user, c)
                    return _twiml(
                        f'Verified! You\'re in {c.name}. '
                        f'Text your actions to play. Try "I look around the room"'
                    )
                return _twiml('Verification failed — user not found.')
            else:
                return _twiml(
                    f'That code didn\'t match. Reply with the campaign join code your DM gave you.'
                )

    # ── Normal gameplay flow ──
    user = User.query.filter_by(phone_number=from_number).first()
    if not user:
        return _twiml(
            'Your phone number is not linked to a campaign. '
            'Ask your DM to add your number in the SMS settings.'
        )

    campaign = None
    character = None

    for c in campaigns:
        state = c.current_state or {}
        if not state.get('sms_enabled'):
            continue
        if user.id in (c.players or []):
            char = Character.query.filter_by(
                user_id=user.id, campaign_id=c.id
            ).first()
            if not char:
                char = Character.query.filter_by(user_id=user.id).first()
            if char:
                campaign = c
                character = char
                break

    if not campaign or not character:
        return _twiml('No active SMS campaign found for your account.')

    response = process_player_sms(body, character, campaign)

    # Bridge to Discord
    try:
        from services.discord_bot import post_to_discord
        post_to_discord(campaign, character.name, body, response, source="sms")
    except Exception:
        pass  # Discord bridge is best-effort

    # After processing, trigger agent responses for any AI-controlled characters
    _trigger_agent_responses(campaign, character, body, response)

    return _twiml(response)


# ── PHONE REGISTRATION (with verification) ──────────────────

@sms_bp.route('/register', methods=['POST'])
def register_phone():
    """
    DM enters a player's phone number. Instead of immediately linking,
    sends a verification SMS with the campaign join code.
    """
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('login'))

    dm = User.query.get(session['user_id'])
    if not dm or dm.role != 'dm':
        flash('DM access required.', 'error')
        return redirect(url_for('index'))

    user_id = request.form.get('user_id', type=int)
    phone = request.form.get('phone_number', '').strip()
    campaign_id = request.form.get('campaign_id', type=int)

    if not user_id or not phone or not campaign_id:
        flash('Missing required fields.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    campaign = Campaign.query.get(campaign_id)
    if not campaign or campaign.dm_id != dm.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    phone = _normalize_phone(phone)

    # Check if phone is already linked to another user
    existing = User.query.filter_by(phone_number=phone).first()
    if existing and existing.id != user_id:
        flash(f'That phone number is already linked to {existing.username}.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    target_user = User.query.get(user_id)
    if not target_user:
        flash('User not found.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    # Store as pending verification
    state = campaign.current_state or {}
    pending = state.get('pending_verifications', {})
    pending[phone] = {
        'user_id': user_id,
        'join_code': campaign.join_code,
        'username': target_user.username,
    }
    state['pending_verifications'] = pending
    campaign.current_state = state
    flag_modified(campaign, 'current_state')
    db.session.commit()

    # Send verification SMS
    from services.sms import send_sms
    char = Character.query.filter_by(user_id=user_id, campaign_id=campaign.id).first()
    if not char:
        char = Character.query.filter_by(user_id=user_id).first()
    char_name = char.name if char else 'an adventurer'

    msg = (
        f"You've been invited to play {campaign.name} as {char_name}!\n\n"
        f"Reply with the campaign code your DM gave you to join.\n\n"
        f"By replying, you agree to receive game messages at this number. "
        f"Text STOP at any time to opt out."
    )
    sid, err = send_sms(phone, msg)

    if err:
        flash(f'Failed to send verification SMS: {err}', 'error')
    else:
        flash(f'Verification SMS sent to {phone}. Waiting for {target_user.username} to reply with the join code.', 'success')

    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@sms_bp.route('/unlink', methods=['POST'])
def unlink_phone():
    """Remove a player's phone number link."""
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('login'))

    dm = User.query.get(session['user_id'])
    if not dm or dm.role != 'dm':
        flash('DM access required.', 'error')
        return redirect(url_for('index'))

    user_id = request.form.get('user_id', type=int)
    campaign_id = request.form.get('campaign_id', type=int)

    campaign = Campaign.query.get(campaign_id)
    if not campaign or campaign.dm_id != dm.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    target_user = User.query.get(user_id)
    if target_user:
        old_phone = target_user.phone_number

        # Send goodbye SMS before unlinking
        if old_phone:
            from services.sms import send_sms
            send_sms(old_phone,
                f"You've been removed from {campaign.name}. "
                f"You will no longer receive game messages at this number."
            )

        target_user.phone_number = None

        # Also remove from pending verifications and agent mode
        state = campaign.current_state or {}
        pending = state.get('pending_verifications', {})
        to_remove = [ph for ph, info in pending.items() if info.get('user_id') == user_id]
        for ph in to_remove:
            del pending[ph]
        agent_players = state.get('agent_mode_players', [])
        if user_id in agent_players:
            agent_players.remove(user_id)
            state['agent_mode_players'] = agent_players
        if to_remove or user_id in (campaign.current_state or {}).get('agent_mode_players', []):
            state['pending_verifications'] = pending
            campaign.current_state = state
            flag_modified(campaign, 'current_state')
        db.session.commit()

        flash(f'Phone number unlinked for {target_user.username}.', 'success')

    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


# ── SMS TOGGLE ───────────────────────────────────────────────

@sms_bp.route('/toggle', methods=['POST'])
def toggle_sms():
    """Toggle SMS play mode on/off for a campaign."""
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('login'))

    campaign_id = request.form.get('campaign_id', type=int)
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    state = campaign.current_state or {}
    state['sms_enabled'] = not state.get('sms_enabled', False)
    campaign.current_state = state
    flag_modified(campaign, 'current_state')
    db.session.commit()

    status = 'enabled' if state['sms_enabled'] else 'disabled'
    flash(f'SMS Play Mode {status}.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


# ── AGENT MODE ───────────────────────────────────────────────

@sms_bp.route('/agent/toggle', methods=['POST'])
def toggle_agent():
    """Toggle AI agent mode for a player's character."""
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('login'))

    dm = User.query.get(session['user_id'])
    if not dm or dm.role != 'dm':
        flash('DM access required.', 'error')
        return redirect(url_for('index'))

    user_id = request.form.get('user_id', type=int)
    campaign_id = request.form.get('campaign_id', type=int)

    campaign = Campaign.query.get(campaign_id)
    if not campaign or campaign.dm_id != dm.id:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    state = campaign.current_state or {}
    agent_players = state.get('agent_mode_players', [])

    if user_id in agent_players:
        agent_players.remove(user_id)
        status = 'disabled'
    else:
        agent_players.append(user_id)
        status = 'enabled'

    state['agent_mode_players'] = agent_players
    campaign.current_state = state
    flag_modified(campaign, 'current_state')
    db.session.commit()

    target_user = User.query.get(user_id)
    name = target_user.username if target_user else 'player'
    flash(f'AI Agent mode {status} for {name}.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


# ── HELPERS ──────────────────────────────────────────────────

def _trigger_agent_responses(campaign, acting_character, player_msg, dm_response):
    """
    After a real player acts, generate responses for any AI-controlled characters.
    """
    state = campaign.current_state or {}
    agent_players = state.get('agent_mode_players', [])
    if not agent_players:
        return

    from services.ai_dm import generate_agent_response, _log_sms

    for agent_user_id in agent_players:
        if agent_user_id == acting_character.user_id:
            continue  # Don't respond to yourself

        char = Character.query.filter_by(user_id=agent_user_id, campaign_id=campaign.id).first()
        if not char:
            char = Character.query.filter_by(user_id=agent_user_id).first()
        if not char:
            continue

        agent_response = generate_agent_response(
            char, campaign, acting_character.name, player_msg, dm_response
        )
        if agent_response:
            _log_sms(campaign, char.name, f'[AI Agent reacting to {acting_character.name}]', agent_response)

            # Send the agent's action through the AI DM for narration
            from services.ai_dm import process_player_sms
            result = process_player_sms(agent_response, char, campaign)
            # Notify the real player about the agent's action via SMS if they have a phone
            agent_user = User.query.get(agent_user_id)
            if agent_user and agent_user.phone_number:
                from services.sms import send_sms
                send_sms(agent_user.phone_number, f'[{char.name} auto-played] {result}')


def _send_welcome_sms(phone, user, campaign):
    """Send a welcome/onboarding SMS to a verified player."""
    from services.sms import send_sms

    char = Character.query.filter_by(user_id=user.id, campaign_id=campaign.id).first()
    if not char:
        char = Character.query.filter_by(user_id=user.id).first()

    if char:
        char_info = f"You're playing as {char.name} (Lv{char.level} {char.race} {char.class_name})."
    else:
        char_info = "Your character is ready."

    msg = (
        f"Welcome to {campaign.name}! {char_info}\n\n"
        f"Text your actions to this number to play. Try:\n"
        f"- \"I look around the room\"\n"
        f"- \"I attack the goblin\"\n"
        f"- \"I try to persuade the guard\"\n\n"
        f"The AI Dungeon Master will roll dice, resolve your action, "
        f"and narrate what happens. Adventure awaits!"
    )
    send_sms(phone, msg)


def _twiml(message):
    """Return a TwiML XML response."""
    xml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{message}</Message></Response>'
    return xml, 200, {'Content-Type': 'text/xml'}
