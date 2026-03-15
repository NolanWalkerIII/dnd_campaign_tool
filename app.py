import io
import json
import os
import random
import string
from datetime import datetime, timedelta
from functools import wraps

from dotenv import load_dotenv
load_dotenv()

from flask import (Flask, render_template, redirect, url_for,
                   request, flash, session, send_file, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Character, Campaign, DiceRoller
from parsers import parse_character_md, parse_campaign_md, CHARACTER_TEMPLATE, CAMPAIGN_TEMPLATE
from services.ai import cleanup_narration, generate_narration
import re as _re

from game_data import (
    RACES, CLASSES, BACKGROUNDS, STANDARD_ARRAY,
    ABILITY_SCORES, ABILITY_NAMES, SKILLS,
    get_spell_slots, SPELLCASTING_TYPE,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dnd-dev-secret-change-in-prod'
db.init_app(app)

with app.app_context():
    db.create_all()
    # Phase 7 migration: add last_seen column if the DB predates it
    with db.engine.connect() as _conn:
        _cols = [r[1] for r in _conn.execute(db.text("PRAGMA table_info('user')"))]
        if 'last_seen' not in _cols:
            _conn.execute(db.text("ALTER TABLE user ADD COLUMN last_seen DATETIME"))
            _conn.commit()


@app.before_request
def update_last_seen():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user.last_seen = datetime.utcnow()
            db.session.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────

def ability_modifier(score):
    return (score - 10) // 2

def mod_str(m):
    return f'+{m}' if m >= 0 else str(m)

def score_mod(score):
    return ability_modifier(score)

def generate_join_code():
    """Generate a unique 6-char uppercase alphanumeric join code."""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Campaign.query.filter_by(join_code=code).first():
            return code

def calculate_ac(class_name, ability_scores):
    cls = CLASSES.get(class_name, {})
    ac_type = cls.get('ac_type', 'unarmored')
    ac_base = cls.get('ac_base', 10)
    shield  = cls.get('shield', False)
    dex_mod = ability_modifier(ability_scores['DEX'])
    con_mod = ability_modifier(ability_scores['CON'])
    wis_mod = ability_modifier(ability_scores['WIS'])
    if ac_type == 'heavy':
        ac = ac_base
    elif ac_type == 'medium':
        ac = ac_base + min(dex_mod, 2)
    elif ac_type == 'light':
        ac = ac_base + dex_mod
    elif ac_type == 'unarmored_barb':
        ac = 10 + dex_mod + con_mod
    elif ac_type == 'unarmored_monk':
        ac = 10 + dex_mod + wis_mod
    else:
        ac = 10 + dex_mod
    if shield:
        ac += 2
    return ac

def calculate_hp(class_name, ability_scores):
    hit_die = CLASSES[class_name]['hit_die']
    con_mod = ability_modifier(ability_scores['CON'])
    return max(1, hit_die + con_mod)

def apply_racial_asi(base_scores, race_name, flex1=None, flex2=None):
    scores = dict(base_scores)
    race = RACES.get(race_name, {})
    for ab, bonus in race.get('asi', {}).items():
        scores[ab] = scores.get(ab, 8) + bonus
    if flex1 and flex1 in scores:
        scores[flex1] += 1
    if flex2 and flex2 in scores:
        scores[flex2] += 1
    return scores

def current_user():
    uid = session.get('user_id')
    if uid:
        return User.query.get(uid)
    return None


# ── Auth decorators ───────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def dm_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'dm':
            flash('Dungeon Master access required.', 'error')
            return redirect(url_for('player_dashboard'))
        return f(*args, **kwargs)
    return decorated

def player_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        role = session.get('role')
        # Allow DMs through when they are impersonating a player
        if role == 'dm' and 'impersonating_user_id' in session:
            return f(*args, **kwargs)
        if role != 'player':
            flash('Player access required.', 'error')
            return redirect(url_for('dm_dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── Template context ──────────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    return dict(
        score_mod=score_mod,
        mod_str=mod_str,
        ability_names=ABILITY_NAMES,
        ability_order=ABILITY_SCORES,
        current_user=current_user(),
        session=session,
    )


# ── Root ──────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') == 'dm':
        return redirect(url_for('dm_dashboard'))
    return redirect(url_for('player_dashboard'))


# ── Auth routes ───────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')
        role     = request.form.get('role', 'player')

        if not username or not password:
            flash('Username and password are required.', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif role not in ('dm', 'player'):
            flash('Invalid role.', 'error')
        elif User.query.filter_by(username=username).first():
            flash('That username is already taken.', 'error')
        else:
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# ── Character routes (shared) ─────────────────────────────────────────────────

@app.route('/characters')
@login_required
def character_list():
    if session.get('role') == 'dm':
        characters = Character.query.order_by(Character.id.desc()).all()
    else:
        characters = Character.query.filter_by(
            user_id=session['user_id']
        ).order_by(Character.id.desc()).all()
    return render_template('characters.html', characters=characters)


@app.route('/characters/new', methods=['GET', 'POST'])
@login_required
def character_new():
    if request.method == 'POST':
        return _create_character()
    return render_template(
        'character_create.html',
        races=RACES,
        classes=CLASSES,
        backgrounds=BACKGROUNDS,
        standard_array=STANDARD_ARRAY,
        ability_scores=ABILITY_SCORES,
        ability_names=ABILITY_NAMES,
        races_json=json.dumps({
            name: {
                'asi': data['asi'],
                'flex_asi': data.get('flex_asi', 0),
                'speed': data['speed'],
                'traits': data['traits'],
                'languages': data['languages'],
            }
            for name, data in RACES.items()
        }),
        classes_json=json.dumps({
            name: {
                'hit_die': data['hit_die'],
                'saving_throws': data['saving_throws'],
                'armor_proficiencies': data['armor_proficiencies'],
                'weapon_proficiencies': data['weapon_proficiencies'],
                'skill_options': data['skill_options'],
                'num_skills': data['num_skills'],
                'spellcasting': data.get('spellcasting'),
            }
            for name, data in CLASSES.items()
        }),
        bgs_json=json.dumps({
            name: {
                'skills': data['skills'],
                'feature': data['feature'],
                'equipment': data['equipment'],
            }
            for name, data in BACKGROUNDS.items()
        }),
        skills_json=json.dumps(SKILLS),
        ability_scores_json=json.dumps(ABILITY_SCORES),
    )


@app.route('/characters/template')
@login_required
def character_template_download():
    buf = io.BytesIO(CHARACTER_TEMPLATE.encode('utf-8'))
    return send_file(buf, as_attachment=True,
                     download_name='character_template.md',
                     mimetype='text/markdown')


@app.route('/characters/import', methods=['POST'])
@login_required
def character_import():
    f = request.files.get('md_file')
    if not f or not f.filename:
        flash('Please choose a markdown file to import.', 'error')
        return redirect(url_for('character_new'))

    try:
        text = f.read().decode('utf-8')
    except Exception:
        flash('Could not read file — make sure it is a UTF-8 text file.', 'error')
        return redirect(url_for('character_new'))

    parsed = parse_character_md(text)
    errors = []

    name       = parsed['name']
    race_name  = parsed['race']
    class_name = parsed['class_name']
    background = parsed['background']
    alignment  = parsed.get('alignment', 'True Neutral')

    if not name:                          errors.append('Name is required in the template.')
    if race_name not in RACES:            errors.append(f'Unknown race: "{race_name}". Check spelling.')
    if class_name not in CLASSES:         errors.append(f'Unknown class: "{class_name}". Check spelling.')
    if background not in BACKGROUNDS:     errors.append(f'Unknown background: "{background}". Check spelling.')

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('character_new'))

    # Use scores as-is (import is not restricted to standard array)
    base_scores = {ab: parsed[ab] for ab in ABILITY_SCORES}
    final_scores = apply_racial_asi(base_scores, race_name)

    # Skills: accept any that are valid SKILLS names
    valid_skills = [s for s in parsed['skills'] if s in SKILLS]

    hp_max = calculate_hp(class_name, final_scores)
    ac     = calculate_ac(class_name, final_scores)

    raw_equipment = (CLASSES[class_name]['starting_equipment']
                     + BACKGROUNDS[background]['equipment']
                     + parsed['equipment_extra'])
    starting_gold = parsed['gold']
    equipment = []
    for item in raw_equipment:
        m = _re.match(r'^(\d+)\s*gp$', item.strip(), _re.IGNORECASE)
        if m:
            starting_gold += int(m.group(1))
        else:
            equipment.append(item)

    sc      = CLASSES[class_name].get('spellcasting')
    hit_die = CLASSES[class_name]['hit_die']
    char = Character(
        name=name, race=race_name, class_name=class_name, level=1,
        ability_scores=final_scores,
        hp_max=hp_max, hp_current=hp_max, ac=ac, proficiency_bonus=2,
        skills=valid_skills, equipment=equipment,
        spells={
            'spellcasting': sc,
            'slots': get_spell_slots(class_name, level=1),
            'known': [],
            'concentration': None,
            'hit_dice_max': 1,
            'hit_dice_current': 1,
            'hit_die': hit_die,
            'gold': starting_gold,
        },
        background=background, alignment=alignment,
        user_id=session.get('user_id'),
    )
    db.session.add(char)
    db.session.commit()
    flash(f'{name} imported successfully!', 'success')
    return redirect(url_for('character_sheet', char_id=char.id))


def _create_character():
    name       = request.form.get('name', '').strip()
    race_name  = request.form.get('race', '')
    class_name = request.form.get('class_name', '')
    background = request.form.get('background', '')
    alignment  = request.form.get('alignment', 'True Neutral')
    flex1      = request.form.get('flex_asi_1', '')
    flex2      = request.form.get('flex_asi_2', '')

    errors = []
    if not name:             errors.append('Character name is required.')
    if race_name not in RACES:   errors.append('Invalid race selected.')
    if class_name not in CLASSES: errors.append('Invalid class selected.')
    if background not in BACKGROUNDS: errors.append('Invalid background selected.')

    base_scores = {}
    for ab in ABILITY_SCORES:
        val = request.form.get(f'base_{ab.lower()}', '')
        try:
            v = int(val)
            if v not in STANDARD_ARRAY:
                errors.append(f'{ab}: invalid value.')
            base_scores[ab] = v
        except (ValueError, TypeError):
            errors.append(f'{ab}: score is required.')

    if len(base_scores) == 6 and sorted(base_scores.values()) != sorted(STANDARD_ARRAY):
        errors.append('Each standard array value must be used exactly once.')

    race_data = RACES.get(race_name, {})
    if race_data.get('flex_asi', 0) > 0:
        if not flex1 or not flex2:
            errors.append('Half-Elf: choose two ability scores for your +1 bonuses.')
        elif flex1 == flex2:
            errors.append('Half-Elf: the two +1 bonus scores must be different.')

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('character_new'))

    final_scores = apply_racial_asi(base_scores, race_name, flex1 or None, flex2 or None)

    selected_skills = request.form.getlist('skills')
    bg_skills   = BACKGROUNDS[background]['skills']
    cls_options = CLASSES[class_name]['skill_options']
    cls_limit   = CLASSES[class_name]['num_skills']
    class_chosen = [s for s in selected_skills if s in cls_options]

    if len(class_chosen) < cls_limit:
        flash(f'Please select {cls_limit} skill proficiencies for your class.', 'error')
        return redirect(url_for('character_new'))

    all_skills = list(set(bg_skills + class_chosen))
    hp_max = calculate_hp(class_name, final_scores)
    ac     = calculate_ac(class_name, final_scores)

    # Combine class + background equipment; parse out gold amounts
    raw_equipment = (CLASSES[class_name]['starting_equipment']
                     + BACKGROUNDS[background]['equipment'])
    starting_gold = 0
    equipment = []
    for item in raw_equipment:
        m = _re.match(r'^(\d+)\s*gp$', item.strip(), _re.IGNORECASE)
        if m:
            starting_gold += int(m.group(1))
        else:
            equipment.append(item)

    sc = CLASSES[class_name].get('spellcasting')
    hit_die = CLASSES[class_name]['hit_die']
    char = Character(
        name=name, race=race_name, class_name=class_name, level=1,
        ability_scores=final_scores,
        hp_max=hp_max, hp_current=hp_max, ac=ac, proficiency_bonus=2,
        skills=all_skills, equipment=equipment,
        spells={
            'spellcasting': sc,
            'slots': get_spell_slots(class_name, level=1),
            'known': [],
            'concentration': None,
            'hit_dice_max': 1,
            'hit_dice_current': 1,
            'hit_die': hit_die,
            'gold': starting_gold,
        },
        background=background, alignment=alignment,
        user_id=session.get('user_id'),
    )
    db.session.add(char)
    db.session.commit()
    flash(f'{name} has been created!', 'success')
    return redirect(url_for('character_sheet', char_id=char.id))


@app.route('/characters/<int:char_id>')
@login_required
def character_sheet(char_id):
    char = Character.query.get_or_404(char_id)
    cls_data  = CLASSES.get(char.class_name, {})
    race_data = RACES.get(char.race, {})
    extra     = char.spells or {}
    sc_ability = extra.get('spellcasting')

    spell_dc = spell_atk = None
    if sc_ability and sc_ability in (char.ability_scores or {}):
        sc_mod    = ability_modifier(char.ability_scores[sc_ability])
        spell_dc  = 8 + char.proficiency_bonus + sc_mod
        spell_atk = char.proficiency_bonus + sc_mod

    # Campaigns this character's owner is in (for DM HP adjustment redirect)
    owner_campaigns = []
    if session.get('role') == 'dm':
        owner_campaigns = Campaign.query.filter_by(dm_id=session['user_id']).all()

    return render_template(
        'character_sheet.html',
        character=char,
        hit_die=cls_data.get('hit_die', 8),
        race_speed=race_data.get('speed', 30),
        race_traits=race_data.get('traits', []),
        saving_throw_profs=cls_data.get('saving_throws', []),
        armor_profs=cls_data.get('armor_proficiencies', []),
        weapon_profs=cls_data.get('weapon_proficiencies', []),
        skills_sorted=sorted(SKILLS.items()),
        spellcasting_ability=sc_ability,
        spell_dc=spell_dc,
        spell_atk=spell_atk,
        owner_campaigns=owner_campaigns,
    )


@app.route('/characters/<int:char_id>/delete')
@login_required
def character_delete(char_id):
    char = Character.query.get_or_404(char_id)
    # Only owner or DM can delete
    if char.user_id != session.get('user_id') and session.get('role') != 'dm':
        flash('You do not have permission to delete this character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))
    name = char.name
    db.session.delete(char)
    db.session.commit()
    flash(f'{name} has been deleted.', 'success')
    return redirect(url_for('character_list'))


# ── DM routes ─────────────────────────────────────────────────────────────────

@app.route('/dm/dashboard')
@dm_required
def dm_dashboard():
    campaigns = Campaign.query.filter_by(dm_id=session['user_id']).all()
    all_chars = Character.query.order_by(Character.id.desc()).all()

    # Players seen within the last 5 minutes are considered online
    cutoff = datetime.utcnow() - timedelta(minutes=5)
    online_players = (User.query
                      .filter(User.role == 'player',
                              User.last_seen >= cutoff)
                      .all())
    # Attach their most recent character for the panel
    for p in online_players:
        p._recent_char = Character.query.filter_by(user_id=p.id).order_by(Character.id.desc()).first()

    return render_template('dm/dashboard.html',
                           campaigns=campaigns, all_chars=all_chars,
                           online_players=online_players)


@app.route('/dm/campaigns/new', methods=['POST'])
@dm_required
def dm_campaign_new():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Campaign name is required.', 'error')
        return redirect(url_for('dm_dashboard'))
    campaign = Campaign(
        name=name,
        dm_id=session['user_id'],
        join_code=generate_join_code(),
        players=[],
        npcs=[],
        current_state={'initiative_order': [], 'active_conditions': {}, 'narration_log': []},
        is_active=True,
    )
    db.session.add(campaign)
    db.session.commit()
    flash(f'Campaign "{name}" created! Share join code: {campaign.join_code}', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign.id))


@app.route('/dm/campaigns/template')
@dm_required
def campaign_template_download():
    buf = io.BytesIO(CAMPAIGN_TEMPLATE.encode('utf-8'))
    return send_file(buf, as_attachment=True,
                     download_name='campaign_template.md',
                     mimetype='text/markdown')


@app.route('/dm/campaigns/import', methods=['POST'])
@dm_required
def campaign_import():
    f = request.files.get('md_file')
    if not f or not f.filename:
        flash('Please choose a markdown file to import.', 'error')
        return redirect(url_for('dm_dashboard'))

    try:
        text = f.read().decode('utf-8')
    except Exception:
        flash('Could not read file — make sure it is a UTF-8 text file.', 'error')
        return redirect(url_for('dm_dashboard'))

    parsed = parse_campaign_md(text)
    camp_name = parsed['name'].strip()
    if not camp_name:
        flash('Campaign name is required in the template.', 'error')
        return redirect(url_for('dm_dashboard'))

    # Build opening narration log entry if narration text was provided
    narration_log = []
    if parsed['opening_narration']:
        narration_log.append({
            'text': parsed['opening_narration'],
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
        })

    campaign = Campaign(
        name=camp_name,
        dm_id=session['user_id'],
        join_code=generate_join_code(),
        players=[],
        npcs=[],
        current_state={
            'initiative_order': [],
            'active_conditions': {},
            'narration_log': narration_log,
            'combat_log': [],
            'npc_presets': parsed['npc_presets'],
        },
        is_active=True,
    )
    db.session.add(campaign)
    db.session.commit()

    npc_count = len(parsed['npc_presets'])
    npc_msg = f', {npc_count} NPC preset(s) loaded' if npc_count else ''
    flash(f'Campaign "{camp_name}" imported! Join code: {campaign.join_code}{npc_msg}', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign.id))


@app.route('/dm/campaigns/<int:campaign_id>')
@dm_required
def dm_campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    # Collect player users and their characters
    player_ids = campaign.players or []
    players = User.query.filter(User.id.in_(player_ids)).all() if player_ids else []
    player_chars = {
        p.id: Character.query.filter_by(user_id=p.id).all()
        for p in players
    }
    state = campaign.current_state or {}
    narration_log = state.get('narration_log', [])

    # Pre-fetch Character objects for combatants in initiative order
    combatant_chars = {}
    for entry in state.get('initiative_order', []):
        cid = entry.get('char_id')
        if cid and not entry.get('is_npc'):
            combatant_chars[cid] = Character.query.get(cid)

    return render_template('dm/campaign.html',
                           campaign=campaign,
                           players=players,
                           player_chars=player_chars,
                           narration_log=narration_log,
                           combatant_chars=combatant_chars,
                           conditions=CONDITIONS,
                           skills_sorted=sorted(SKILLS.keys()))


@app.route('/dm/campaigns/<int:campaign_id>/narrate', methods=['POST'])
@dm_required
def dm_narrate(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    text = request.form.get('narration', '').strip()
    if text:
        state = campaign.current_state or {}
        log = state.get('narration_log', [])
        log.append({'text': text, 'timestamp': datetime.now().strftime('%b %d, %H:%M')})
        state['narration_log'] = log
        campaign.current_state = state
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(campaign, 'current_state')
        db.session.commit()

    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/ai/cleanup', methods=['POST'])
@dm_required
def dm_ai_cleanup(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        return jsonify({'error': 'Access denied.'}), 403

    raw = request.json.get('text', '').strip() if request.is_json else ''
    if not raw:
        return jsonify({'error': 'No text provided.'}), 400

    text, error = cleanup_narration(raw)
    if error:
        return jsonify({'error': error}), 502
    return jsonify({'text': text})


@app.route('/dm/campaigns/<int:campaign_id>/ai/generate', methods=['POST'])
@dm_required
def dm_ai_generate(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        return jsonify({'error': 'Access denied.'}), 403

    narration_log = (campaign.current_state or {}).get('narration_log', [])
    text, error = generate_narration(narration_log)
    if error:
        return jsonify({'error': error}), 502
    return jsonify({'text': text})


@app.route('/dm/campaigns/<int:campaign_id>/save')
@dm_required
def dm_campaign_save(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    # Collect all player characters for this campaign
    player_ids = campaign.players or []
    char_snapshots = []
    for uid in player_ids:
        for char in Character.query.filter_by(user_id=uid).all():
            char_snapshots.append({
                'id':             char.id,
                'name':           char.name,
                'race':           char.race,
                'class_name':     char.class_name,
                'level':          char.level,
                'ability_scores': char.ability_scores,
                'hp_max':         char.hp_max,
                'hp_current':     char.hp_current,
                'ac':             char.ac,
                'proficiency_bonus': char.proficiency_bonus,
                'skills':         char.skills,
                'equipment':      char.equipment,
                'spells':         char.spells,
                'background':     char.background,
                'alignment':      char.alignment,
                'user_id':        char.user_id,
            })

    save_data = {
        'schema_version': 1,
        'saved_at':       datetime.utcnow().isoformat(),
        'campaign': {
            'id':            campaign.id,
            'name':          campaign.name,
            'join_code':     campaign.join_code,
            'players':       campaign.players,
            'npcs':          campaign.npcs,
            'current_state': campaign.current_state,
            'is_active':     campaign.is_active,
        },
        'characters': char_snapshots,
    }

    filename = (campaign.name.lower().replace(' ', '_')[:30]
                + '_' + datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                + '.json')
    buf = io.BytesIO(json.dumps(save_data, indent=2).encode('utf-8'))
    return send_file(buf, as_attachment=True,
                     download_name=filename,
                     mimetype='application/json')


@app.route('/dm/campaigns/<int:campaign_id>/load', methods=['POST'])
@dm_required
def dm_campaign_load(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    f = request.files.get('save_file')
    if not f or not f.filename:
        flash('Please choose a save file to load.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    try:
        save_data = json.loads(f.read().decode('utf-8'))
    except Exception:
        flash('Could not read save file — make sure it is a valid JSON file.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    if save_data.get('schema_version') != 1:
        flash('Unrecognised save file format.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    saved_campaign = save_data.get('campaign', {})
    if saved_campaign.get('id') != campaign_id:
        flash('This save file is for a different campaign.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    # Restore campaign state
    campaign.current_state = saved_campaign.get('current_state', {})
    campaign.players       = saved_campaign.get('players', [])
    campaign.npcs          = saved_campaign.get('npcs', [])
    campaign.is_active     = saved_campaign.get('is_active', True)
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(campaign, 'current_state')
    flag_modified(campaign, 'players')

    # Restore character HP and spell slots for each saved character
    restored = 0
    for snap in save_data.get('characters', []):
        char = Character.query.get(snap['id'])
        if char and char.user_id in (campaign.players or []):
            char.hp_current = snap.get('hp_current', char.hp_current)
            char.hp_max     = snap.get('hp_max', char.hp_max)
            char.spells     = snap.get('spells', char.spells)
            char.equipment  = snap.get('equipment', char.equipment)
            flag_modified(char, 'spells')
            flag_modified(char, 'equipment')
            restored += 1

    db.session.commit()
    flash(f'Campaign restored from save. '
          f'{restored} character(s) updated.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/toggle', methods=['POST'])
@dm_required
def dm_campaign_toggle(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))
    campaign.is_active = not campaign.is_active
    db.session.commit()
    status = 'activated' if campaign.is_active else 'deactivated'
    flash(f'Campaign {status}.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/characters/<int:char_id>/hp', methods=['POST'])
@dm_required
def dm_adjust_hp(char_id):
    char = Character.query.get_or_404(char_id)
    campaign_id = request.form.get('campaign_id', type=int)
    try:
        delta = int(request.form.get('delta', 0))
    except (ValueError, TypeError):
        delta = 0

    char.hp_current = max(0, min(char.hp_max, char.hp_current + delta))
    db.session.commit()

    action = f'Healed {delta} HP' if delta > 0 else f'Dealt {abs(delta)} damage'
    flash(f'{char.name}: {action}. HP now {char.hp_current}/{char.hp_max}.', 'success')

    if campaign_id:
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))
    return redirect(url_for('character_sheet', char_id=char_id))


# ── DM Impersonation routes ───────────────────────────────────────────────────

@app.route('/dm/impersonate/<int:user_id>/campaign/<int:campaign_id>')
@dm_required
def dm_impersonate(user_id, campaign_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'player':
        flash('Can only impersonate players.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))
    session['impersonating_user_id'] = user_id
    session['impersonating_username'] = user.username
    return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/impersonate/exit')
def dm_impersonate_exit():
    campaign_id = request.args.get('campaign_id', type=int)
    session.pop('impersonating_user_id', None)
    session.pop('impersonating_username', None)
    if campaign_id:
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))
    return redirect(url_for('dm_dashboard'))


# ── Player routes ─────────────────────────────────────────────────────────────

@app.route('/player/dashboard')
@player_required
def player_dashboard():
    my_chars = Character.query.filter_by(
        user_id=session['user_id']
    ).order_by(Character.id.desc()).all()

    all_campaigns = Campaign.query.all()
    my_campaigns = [c for c in all_campaigns
                    if session['user_id'] in (c.players or [])]

    return render_template('player/dashboard.html',
                           my_chars=my_chars,
                           my_campaigns=my_campaigns)


@app.route('/player/campaigns/join', methods=['POST'])
@player_required
def player_join_campaign():
    code = request.form.get('join_code', '').strip().upper()
    campaign = Campaign.query.filter_by(join_code=code).first()

    if not campaign:
        flash(f'No campaign found with code "{code}".', 'error')
        return redirect(url_for('player_dashboard'))
    if not campaign.is_active:
        flash('That campaign is not currently active.', 'error')
        return redirect(url_for('player_dashboard'))

    players = list(campaign.players or [])
    if session['user_id'] in players:
        flash('You have already joined this campaign.', 'success')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign.id))

    players.append(session['user_id'])
    campaign.players = players
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(campaign, 'players')
    db.session.commit()
    flash(f'You joined "{campaign.name}"!', 'success')
    return redirect(url_for('player_campaign_detail', campaign_id=campaign.id))


@app.route('/player/campaigns/<int:campaign_id>')
@player_required
def player_campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # When the DM is impersonating, view the campaign from that player's perspective
    uid = _effective_uid()
    if uid not in (campaign.players or []):
        flash('You are not in this campaign.', 'error')
        return redirect(url_for('player_dashboard'))

    dm = User.query.get(campaign.dm_id) if campaign.dm_id else None
    my_chars = Character.query.filter_by(user_id=uid).all()
    narration_log = (campaign.current_state or {}).get('narration_log', [])

    # Determine active character's spell slots for the action panel
    active_char = _get_player_active_char(campaign_id)
    active_slots = (active_char.spells or {}).get('slots', {}) if active_char else {}

    return render_template('player/campaign.html',
                           campaign=campaign,
                           dm=dm,
                           my_chars=my_chars,
                           narration_log=narration_log,
                           skills_sorted=sorted(SKILLS.keys()),
                           active_slots=active_slots,
                           view_uid=uid)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ordinal(n):
    if n in (11, 12, 13):
        return f'{n}th'
    return f'{n}{["th","st","nd","rd","th","th","th","th","th","th"][n % 10]}'

def _flag(obj, col):
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(obj, col)

def _char_owned(char):
    return char.user_id == session.get('user_id') or session.get('role') == 'dm'


# ── Spell casting ─────────────────────────────────────────────────────────────

@app.route('/characters/<int:char_id>/cast', methods=['POST'])
@login_required
def character_cast_spell(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    try:
        slot_level = str(int(request.form.get('slot_level', 1)))
    except (ValueError, TypeError):
        flash('Invalid slot level.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    spell_name     = request.form.get('spell_name', '').strip() or f'{_ordinal(int(slot_level))}-level spell'
    is_conc        = 'concentration' in request.form
    extra          = dict(char.spells or {})
    slots          = extra.get('slots', {})

    if slot_level not in slots or slots[slot_level]['current'] <= 0:
        flash(f'No {_ordinal(int(slot_level))}-level slots remaining.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    slots[slot_level]['current'] -= 1
    extra['slots'] = slots
    if is_conc:
        extra['concentration'] = spell_name
    char.spells = extra
    _flag(char, 'spells')
    db.session.commit()

    rem = slots[slot_level]['current']
    mx  = slots[slot_level]['max']
    conc_tag = ' — Concentrating' if is_conc else ''
    flash(f'Cast {spell_name} ({_ordinal(int(slot_level))}-level){conc_tag}. '
          f'Slots remaining: {rem}/{mx}.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


@app.route('/characters/<int:char_id>/concentration/clear', methods=['POST'])
@login_required
def character_clear_concentration(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))
    extra = dict(char.spells or {})
    extra['concentration'] = None
    char.spells = extra
    _flag(char, 'spells')
    db.session.commit()
    flash('Concentration dropped.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


# Campaign-context cast (expends slot + logs to combat log)
@app.route('/player/campaigns/<int:campaign_id>/cast', methods=['POST'])
@player_required
def player_cast_spell(campaign_id):
    blocked = _check_not_impersonating(campaign_id)
    if blocked:
        return blocked
    campaign = Campaign.query.get_or_404(campaign_id)
    if session['user_id'] not in (campaign.players or []):
        flash('Not in this campaign.', 'error')
        return redirect(url_for('player_dashboard'))

    char = _get_player_active_char(campaign_id)
    if not char:
        flash('No character found.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    try:
        slot_level = str(int(request.form.get('slot_level', 1)))
    except (ValueError, TypeError):
        flash('Invalid slot level.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    spell_name = request.form.get('spell_name', '').strip() or f'{_ordinal(int(slot_level))}-level spell'
    is_conc    = 'concentration' in request.form
    extra      = dict(char.spells or {})
    slots      = extra.get('slots', {})

    if slot_level not in slots or slots[slot_level]['current'] <= 0:
        flash(f'No {_ordinal(int(slot_level))}-level slots remaining.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    slots[slot_level]['current'] -= 1
    extra['slots'] = slots
    if is_conc:
        extra['concentration'] = spell_name
    char.spells = extra
    _flag(char, 'spells')

    conc_tag = ' (Concentration)' if is_conc else ''
    text = f'casts {spell_name} using a {_ordinal(int(slot_level))}-level slot{conc_tag}.'
    _add_combat_log(campaign, char.name, text, 'roll')
    _save_state(campaign)
    db.session.commit()

    flash(f'Cast {spell_name}! Slot {slot_level}: '
          f'{slots[slot_level]["current"]}/{slots[slot_level]["max"]} remaining.', 'success')
    return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))


# ── Rest system ───────────────────────────────────────────────────────────────

@app.route('/characters/<int:char_id>/rest/short', methods=['POST'])
@login_required
def character_rest_short(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    extra = dict(char.spells or {})
    hit_die          = extra.get('hit_die', CLASSES.get(char.class_name, {}).get('hit_die', 8))
    hit_dice_current = extra.get('hit_dice_current', 1)

    if hit_dice_current <= 0:
        flash('No hit dice remaining. Take a long rest to recover them.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    try:
        num = max(1, min(int(request.form.get('num_dice', 1)), hit_dice_current))
    except (ValueError, TypeError):
        num = 1

    con_mod   = ability_modifier((char.ability_scores or {}).get('CON', 10))
    total_heal = sum(max(1, DiceRoller.roll(f'1d{hit_die}', modifier=con_mod)[0]) for _ in range(num))
    old_hp    = char.hp_current
    char.hp_current = min(char.hp_max, char.hp_current + total_heal)
    healed    = char.hp_current - old_hp

    extra['hit_dice_current'] = hit_dice_current - num

    # Warlock recovers all spell slots on a short rest
    is_warlock = char.class_name == 'Warlock'
    if is_warlock:
        slots = extra.get('slots', {})
        for sl in slots:
            slots[sl]['current'] = slots[sl]['max']
        extra['slots'] = slots

    char.spells = extra
    _flag(char, 'spells')
    db.session.commit()

    die_word = 'die' if num == 1 else 'dice'
    slot_msg = ' Warlock spell slots restored!' if is_warlock else ''
    flash(f'Short rest: spent {num} hit {die_word} (d{hit_die}), healed {healed} HP.{slot_msg}', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


@app.route('/characters/<int:char_id>/rest/long', methods=['POST'])
@login_required
def character_rest_long(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    extra = dict(char.spells or {})

    char.hp_current = char.hp_max

    # Restore all spell slots
    slots = extra.get('slots', {})
    for sl in slots:
        slots[sl]['current'] = slots[sl]['max']
    extra['slots'] = slots

    # Restore hit dice (regain half max, min 1)
    hd_max     = extra.get('hit_dice_max', char.level)
    hd_current = extra.get('hit_dice_current', hd_max)
    regain     = max(1, hd_max // 2)
    extra['hit_dice_current'] = min(hd_max, hd_current + regain)

    extra['concentration'] = None
    char.spells = extra
    _flag(char, 'spells')
    db.session.commit()

    die_word = 'die' if regain == 1 else 'dice'
    flash(f'Long rest complete! HP fully restored, all spell slots recovered, '
          f'{regain} hit {die_word} regained.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


# ── Inventory & gold ──────────────────────────────────────────────────────────

@app.route('/characters/<int:char_id>/inventory/add', methods=['POST'])
@login_required
def inventory_add(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    item = request.form.get('item', '').strip()
    if not item:
        flash('Item name is required.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    equip = list(char.equipment or [])
    equip.append(item)
    char.equipment = equip
    _flag(char, 'equipment')
    db.session.commit()
    flash(f'"{item}" added to inventory.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


@app.route('/characters/<int:char_id>/inventory/remove/<int:idx>', methods=['POST'])
@login_required
def inventory_remove(char_id, idx):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    equip = list(char.equipment or [])
    if 0 <= idx < len(equip):
        removed = equip.pop(idx)
        char.equipment = equip
        _flag(char, 'equipment')
        db.session.commit()
        flash(f'"{removed}" removed from inventory.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


@app.route('/characters/<int:char_id>/gold', methods=['POST'])
@login_required
def adjust_gold(char_id):
    char = Character.query.get_or_404(char_id)
    if not _char_owned(char):
        flash('Not your character.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    try:
        delta = int(request.form.get('delta', 0))
    except (ValueError, TypeError):
        flash('Invalid gold amount.', 'error')
        return redirect(url_for('character_sheet', char_id=char_id))

    extra = dict(char.spells or {})
    old_gold = extra.get('gold', 0)
    new_gold = max(0, old_gold + delta)
    extra['gold'] = new_gold
    char.spells = extra
    _flag(char, 'spells')
    db.session.commit()

    action = f'Gained {delta} gp' if delta > 0 else f'Spent {abs(delta)} gp'
    flash(f'{action}. Gold: {new_gold} gp.', 'success')
    return redirect(url_for('character_sheet', char_id=char_id))


CONDITIONS = [
    'Blinded', 'Charmed', 'Deafened', 'Frightened', 'Grappled',
    'Incapacitated', 'Invisible', 'Paralyzed', 'Petrified', 'Poisoned',
    'Prone', 'Restrained', 'Stunned', 'Unconscious',
]


# ── Combat helpers ────────────────────────────────────────────────────────────

def _save_state(campaign):
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(campaign, 'current_state')
    db.session.commit()


def _add_combat_log(campaign, actor, text, log_type='roll'):
    state = campaign.current_state or {}
    log = state.get('combat_log', [])
    log.append({
        'actor': actor,
        'text': text,
        'timestamp': datetime.now().strftime('%H:%M'),
        'type': log_type,
    })
    state['combat_log'] = log
    campaign.current_state = state


def _get_combatant_conditions(state, key):
    return state.get('active_conditions', {}).get(str(key), [])


def _char_attack_bonus(char, ability='STR'):
    score = (char.ability_scores or {}).get(ability, 10)
    return char.proficiency_bonus + ability_modifier(score)


# ── DM combat routes ──────────────────────────────────────────────────────────

@app.route('/dm/campaigns/<int:campaign_id>/combat/start', methods=['POST'])
@dm_required
def dm_combat_start(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    state = campaign.current_state or {}
    player_ids = campaign.players or []

    # Roll initiative for each player's active character
    order = []
    for uid in player_ids:
        char = Character.query.filter_by(user_id=uid).order_by(Character.id.desc()).first()
        if not char:
            continue
        dex_mod = ability_modifier((char.ability_scores or {}).get('DEX', 10))
        roll, rolls, _ = DiceRoller.roll('1d20', modifier=dex_mod)
        order.append({
            'name': char.name,
            'char_id': char.id,
            'user_id': uid,
            'initiative': roll,
            'roll_detail': f'd20({rolls[0]}){mod_str(dex_mod)}={roll}',
            'is_npc': False,
            'npc_hp': None, 'npc_hp_max': None, 'npc_ac': None,
        })

    order.sort(key=lambda x: x['initiative'], reverse=True)
    state['initiative_order'] = order
    state['turn_index'] = 0
    state['round'] = 1
    state['combat_active'] = True
    state.setdefault('active_conditions', {})
    state.setdefault('death_saves', {})
    state['combat_log'] = []
    campaign.current_state = state

    names = ', '.join(e['name'] for e in order)
    _add_combat_log(campaign, 'System',
                    f'Combat started! Initiative order: {names}', 'system')
    _save_state(campaign)
    flash('Combat started! Initiative rolled for all players.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/npc/add', methods=['POST'])
@dm_required
def dm_npc_add(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.dm_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dm_dashboard'))

    name = request.form.get('npc_name', '').strip()
    try:
        initiative = int(request.form.get('npc_initiative', 10))
        hp = int(request.form.get('npc_hp', 10))
        ac = int(request.form.get('npc_ac', 10))
    except (ValueError, TypeError):
        flash('Invalid NPC stats.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    if not name:
        flash('NPC name is required.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    state = campaign.current_state or {}
    order = state.get('initiative_order', [])
    order.append({
        'name': name, 'char_id': None, 'user_id': None,
        'initiative': initiative, 'roll_detail': str(initiative),
        'is_npc': True, 'npc_hp': hp, 'npc_hp_max': hp, 'npc_ac': ac,
    })
    order.sort(key=lambda x: x['initiative'], reverse=True)
    state['initiative_order'] = order
    campaign.current_state = state
    _add_combat_log(campaign, 'System', f'{name} joins combat (Initiative {initiative}).', 'system')
    _save_state(campaign)
    flash(f'{name} added to combat.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/combat/next', methods=['POST'])
@dm_required
def dm_combat_next(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    state = campaign.current_state or {}
    order = state.get('initiative_order', [])
    if not order:
        flash('No combatants in initiative order.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    idx = state.get('turn_index', 0)
    idx = (idx + 1) % len(order)
    if idx == 0:
        state['round'] = state.get('round', 1) + 1
        _add_combat_log(campaign, 'System',
                        f'Round {state["round"]} begins.', 'system')

    state['turn_index'] = idx
    campaign.current_state = state

    current = order[idx]
    # Trigger death save if HP = 0 (PC only)
    if not current['is_npc'] and current['char_id']:
        char = Character.query.get(current['char_id'])
        if char and char.hp_current <= 0:
            saves = state.setdefault('death_saves', {})
            key = str(current['char_id'])
            ds = saves.get(key, {'successes': 0, 'failures': 0})
            roll, rolls, _ = DiceRoller.roll('1d20')
            if rolls[0] == 20:
                char.hp_current = 1
                db.session.add(char)
                ds = {'successes': 0, 'failures': 0}
                _add_combat_log(campaign, current['name'],
                                f'Death save — nat 20! Regains 1 HP and is stable.', 'system')
            elif rolls[0] == 1:
                ds['failures'] = ds.get('failures', 0) + 2
                _add_combat_log(campaign, current['name'],
                                f'Death save — nat 1! Two failures ({ds["failures"]}/3).', 'system')
            elif rolls[0] >= 10:
                ds['successes'] = ds.get('successes', 0) + 1
                _add_combat_log(campaign, current['name'],
                                f'Death save — {rolls[0]} ✓ ({ds["successes"]}/3 successes).', 'system')
            else:
                ds['failures'] = ds.get('failures', 0) + 1
                _add_combat_log(campaign, current['name'],
                                f'Death save — {rolls[0]} ✗ ({ds["failures"]}/3 failures).', 'system')

            if ds.get('successes', 0) >= 3:
                ds = {'successes': 0, 'failures': 0}
                _add_combat_log(campaign, current['name'], 'Stable! (3 successes)', 'system')
            elif ds.get('failures', 0) >= 3:
                _add_combat_log(campaign, current['name'], 'Dead. (3 failures)', 'system')

            saves[key] = ds
            state['death_saves'] = saves

    _save_state(campaign)
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/combat/end', methods=['POST'])
@dm_required
def dm_combat_end(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    state = campaign.current_state or {}
    state['combat_active'] = False
    campaign.current_state = state
    _add_combat_log(campaign, 'System', 'Combat ended.', 'system')
    _save_state(campaign)
    flash('Combat ended.', 'success')
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/npc/<int:order_idx>/hp', methods=['POST'])
@dm_required
def dm_npc_hp(campaign_id, order_idx):
    campaign = Campaign.query.get_or_404(campaign_id)
    state = campaign.current_state or {}
    order = state.get('initiative_order', [])

    if order_idx >= len(order) or not order[order_idx].get('is_npc'):
        flash('NPC not found.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    try:
        delta = int(request.form.get('delta', 0))
    except (ValueError, TypeError):
        delta = 0

    target = order[order_idx]
    old_hp = target['npc_hp']
    new_hp = max(0, min(target['npc_hp_max'], old_hp + delta))
    order[order_idx]['npc_hp'] = new_hp

    state['initiative_order'] = order
    campaign.current_state = state
    action = f'healed {delta} HP' if delta > 0 else f'took {abs(delta)} damage'
    _add_combat_log(campaign, 'DM', f'{target["name"]} {action}. HP: {new_hp}/{target["npc_hp_max"]}', 'system')
    _save_state(campaign)
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


@app.route('/dm/campaigns/<int:campaign_id>/conditions', methods=['POST'])
@dm_required
def dm_set_condition(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    state = campaign.current_state or {}
    conditions = state.setdefault('active_conditions', {})

    target_key = request.form.get('target_key', '')
    condition   = request.form.get('condition', '')
    action      = request.form.get('action', 'add')  # 'add' or 'remove'
    target_name = request.form.get('target_name', target_key)

    if not target_key or condition not in CONDITIONS:
        flash('Invalid condition or target.', 'error')
        return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))

    conds = conditions.get(str(target_key), [])
    if action == 'add' and condition not in conds:
        conds.append(condition)
        _add_combat_log(campaign, 'DM', f'{target_name} is now {condition}.', 'system')
    elif action == 'remove' and condition in conds:
        conds.remove(condition)
        _add_combat_log(campaign, 'DM', f'{target_name} is no longer {condition}.', 'system')

    conditions[str(target_key)] = conds
    state['active_conditions'] = conditions
    campaign.current_state = state
    _save_state(campaign)
    return redirect(url_for('dm_campaign_detail', campaign_id=campaign_id))


# ── Player action routes ──────────────────────────────────────────────────────

def _effective_uid():
    """Return the impersonated player's user_id if the DM is impersonating, else the real user_id."""
    return session.get('impersonating_user_id', session['user_id'])


def _check_not_impersonating(campaign_id):
    """Return a redirect response if the DM is impersonating (actions blocked), else None."""
    if 'impersonating_user_id' in session:
        flash('Actions are disabled while viewing as a player.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))
    return None


def _get_player_active_char(campaign_id):
    """Return the player's character that is in the initiative order, else most recent."""
    from models import Character
    state = Campaign.query.get(campaign_id).current_state or {}
    order = state.get('initiative_order', [])
    uid = _effective_uid()
    for entry in order:
        if entry.get('user_id') == uid and entry.get('char_id'):
            return Character.query.get(entry['char_id'])
    return Character.query.filter_by(user_id=uid).order_by(Character.id.desc()).first()


def _is_players_turn(campaign):
    state = campaign.current_state or {}
    if not state.get('combat_active'):
        return False
    order = state.get('initiative_order', [])
    idx = state.get('turn_index', 0)
    if not order or idx >= len(order):
        return False
    current = order[idx]
    return current.get('user_id') == _effective_uid()


@app.route('/player/campaigns/<int:campaign_id>/roll', methods=['POST'])
@player_required
def player_roll(campaign_id):
    blocked = _check_not_impersonating(campaign_id)
    if blocked:
        return blocked
    campaign = Campaign.query.get_or_404(campaign_id)
    if session['user_id'] not in (campaign.players or []):
        flash('Not in this campaign.', 'error')
        return redirect(url_for('player_dashboard'))

    dice_str = request.form.get('dice', '1d20').strip()
    char = _get_player_active_char(campaign_id)
    actor = char.name if char else session['username']

    try:
        total, label, rolls, modifier, is_crit = DiceRoller.parse_and_roll(dice_str)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    crit_tag = ' — CRITICAL!' if is_crit else ''
    text = f'rolled {label} → [{", ".join(str(r) for r in rolls)}]{crit_tag} = {total}'
    _add_combat_log(campaign, actor, text, 'roll')
    _save_state(campaign)
    flash(f'{label}: {total}{crit_tag}', 'success')
    return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))


@app.route('/player/campaigns/<int:campaign_id>/skill', methods=['POST'])
@player_required
def player_skill(campaign_id):
    blocked = _check_not_impersonating(campaign_id)
    if blocked:
        return blocked
    campaign = Campaign.query.get_or_404(campaign_id)
    if session['user_id'] not in (campaign.players or []):
        flash('Not in this campaign.', 'error')
        return redirect(url_for('player_dashboard'))

    skill_name = request.form.get('skill', '')
    char = _get_player_active_char(campaign_id)
    if not char:
        flash('No character found.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    from game_data import SKILLS
    if skill_name not in SKILLS:
        flash('Invalid skill.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    ab = SKILLS[skill_name]
    base = ability_modifier((char.ability_scores or {}).get(ab, 10))
    prof = char.proficiency_bonus if skill_name in (char.skills or []) else 0

    # Check conditions
    state = campaign.current_state or {}
    conds = _get_combatant_conditions(state, char.id)
    # (no skill disadvantage from conditions in basic implementation)

    total_mod = base + prof
    roll, rolls, _ = DiceRoller.roll('1d20', modifier=total_mod)
    prof_tag = ' (proficient)' if prof else ''
    text = (f'{skill_name} check{prof_tag}: d20({rolls[0]})'
            f'{mod_str(total_mod)} = {roll}')
    _add_combat_log(campaign, char.name, text, 'skill')
    _save_state(campaign)
    flash(f'{skill_name}: {roll}', 'success')
    return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))


@app.route('/player/campaigns/<int:campaign_id>/attack', methods=['POST'])
@player_required
def player_attack(campaign_id):
    blocked = _check_not_impersonating(campaign_id)
    if blocked:
        return blocked
    campaign = Campaign.query.get_or_404(campaign_id)
    if session['user_id'] not in (campaign.players or []):
        flash('Not in this campaign.', 'error')
        return redirect(url_for('player_dashboard'))

    char = _get_player_active_char(campaign_id)
    if not char:
        flash('No character found.', 'error')
        return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))

    target_name = request.form.get('target', 'target').strip() or 'target'
    ability     = request.form.get('ability', 'STR')
    damage_dice = request.form.get('damage_dice', '').strip()
    try:
        target_ac = int(request.form.get('target_ac', '')) if request.form.get('target_ac') else None
    except (ValueError, TypeError):
        target_ac = None

    if ability not in ABILITY_SCORES:
        ability = 'STR'

    # Check conditions for disadvantage
    state = campaign.current_state or {}
    conds = _get_combatant_conditions(state, char.id)
    has_disadvantage = 'Poisoned' in conds or 'Restrained' in conds
    has_advantage = 'Invisible' in conds  # invisible attackers have advantage

    atk_bonus = _char_attack_bonus(char, ability)
    atk_total, rolls, is_crit = DiceRoller.roll('1d20', modifier=atk_bonus,
                                                  advantage=has_advantage,
                                                  disadvantage=has_disadvantage)
    adv_tag = ' (advantage)' if has_advantage else (' (disadvantage)' if has_disadvantage else '')
    crit_tag = ' — CRITICAL HIT!' if is_crit else ''

    hit_tag = ''
    if target_ac is not None:
        hit_tag = ' — HIT!' if atk_total >= target_ac else ' — MISS!'

    atk_text = (f'attacks {target_name}{adv_tag}: d20({rolls[0]})'
                f'{mod_str(atk_bonus)} = {atk_total}{hit_tag}{crit_tag}')

    dmg_text = ''
    if damage_dice and (hit_tag == ' — HIT!' or target_ac is None or is_crit):
        try:
            # Double dice on crit
            dice_str = damage_dice
            if is_crit:
                m = __import__('re').match(r'^(\d+)d(\d+)([+-]\d+)?$',
                                           damage_dice.lower().strip())
                if m:
                    dice_str = f'{int(m.group(1))*2}d{m.group(2)}'
                    if m.group(3):
                        dice_str += m.group(3)
            ability_score = (char.ability_scores or {}).get(ability, 10)
            dmg_mod = ability_modifier(ability_score)
            total_dmg, label, dmg_rolls, _, _ = DiceRoller.parse_and_roll(dice_str)
            # parse_and_roll already added mod from string; add ability mod separately if not in string
            if not __import__('re').search(r'[+-]\d+$', damage_dice.lower().strip()):
                total_dmg += dmg_mod
                label = f'{damage_dice}{mod_str(dmg_mod)}'
            crit_label = ' (crit — doubled dice!)' if is_crit else ''
            dmg_text = f'  Damage: {label} = {total_dmg}{crit_label}'
        except ValueError:
            dmg_text = '  (invalid damage dice)'

    full_text = atk_text + (f'\n{dmg_text}' if dmg_text else '')
    _add_combat_log(campaign, char.name, full_text, 'attack')
    _save_state(campaign)
    flash(f'Attack: {atk_total}{hit_tag}{crit_tag}', 'success')
    return redirect(url_for('player_campaign_detail', campaign_id=campaign_id))


def _migrate():
    """Apply any schema changes that db.create_all() won't add to existing tables."""
    with db.engine.connect() as conn:
        # Phase 7: add last_seen to user table if missing
        cols = [row[1] for row in conn.execute(
            db.text("PRAGMA table_info('user')")
        )]
        if 'last_seen' not in cols:
            conn.execute(db.text("ALTER TABLE user ADD COLUMN last_seen DATETIME"))
            conn.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        _migrate()
    app.run(debug=True)
