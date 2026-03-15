"""
test_suite.py - Comprehensive test suite for D&D Campaign Manager
Covers: dice mechanics, game logic, auth, characters, combat, Phase 5 features
Run: python test_suite.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app as flask_app, db, ability_modifier, calculate_ac, calculate_hp, apply_racial_asi
from models import DiceRoller, Character, Campaign, User
from game_data import get_spell_slots, STANDARD_ARRAY, CLASSES
from werkzeug.security import generate_password_hash
from werkzeug.datastructures import MultiDict

# ── Test configuration ────────────────────────────────────────────────────────
# Must be set before the engine is first used; Flask-SQLAlchemy uses StaticPool
# for sqlite:///:memory: so all connections share the same in-memory database.

flask_app.config.update({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SECRET_KEY': 'test-only-secret',
})


def make_client():
    """Return a fresh Flask test client with an empty in-memory DB."""
    client = flask_app.test_client()
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    return client


def register(client, username, password='pass123', role='player'):
    """Register an account and then log in. Returns the login response."""
    client.post('/register', data={
        'username': username, 'password': password,
        'confirm': password, 'role': role,
    }, follow_redirects=True)
    return client.post('/login', data={
        'username': username, 'password': password,
    }, follow_redirects=True)


def login(client, username, password='pass123'):
    return client.post('/login', data={
        'username': username, 'password': password,
    }, follow_redirects=True)


# Use list-of-tuples for forms with multi-value fields (skills).
# This is the most reliable way to send repeated form keys in Werkzeug.

def fighter_form(name='Arlen'):
    return MultiDict([
        ('name', name),
        ('race', 'Human'),
        ('class_name', 'Fighter'),
        ('background', 'Soldier'),
        ('alignment', 'Lawful Good'),
        ('base_str', '15'), ('base_dex', '14'), ('base_con', '13'),
        ('base_int', '12'), ('base_wis', '10'), ('base_cha', '8'),
        ('skills', 'Athletics'),
        ('skills', 'Perception'),
    ])


def wizard_form(name='Elaryn'):
    return MultiDict([
        ('name', name),
        ('race', 'Human'),
        ('class_name', 'Wizard'),
        ('background', 'Sage'),
        ('alignment', 'Neutral Good'),
        ('base_str', '8'),  ('base_dex', '14'), ('base_con', '13'),
        ('base_int', '15'), ('base_wis', '12'), ('base_cha', '10'),
        ('skills', 'Insight'),
        ('skills', 'Medicine'),
    ])


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 1 — DiceRoller
# ═════════════════════════════════════════════════════════════════════════════

def test_parse_and_roll_valid():
    cases = [
        ('1d20', 1, 20),
        ('2d6+3', 5, 15),
        ('d8', 1, 8),
        ('d8-1', 0, 7),
        ('3d4', 3, 12),
    ]
    for expr, lo, hi in cases:
        total, label, rolls, mod, is_crit = DiceRoller.parse_and_roll(expr)
        assert lo <= total <= hi, f'{expr}: total {total} not in [{lo}, {hi}]'
    print('  parse_and_roll accepts valid expressions')


def test_parse_and_roll_invalid():
    bad = ['asdf', '', '0d6', '1d1', '1000d20', '1d0']
    for expr in bad:
        try:
            DiceRoller.parse_and_roll(expr)
            assert False, f'Expected ValueError for "{expr}"'
        except ValueError:
            pass
    print(f'  parse_and_roll rejects {len(bad)} invalid expressions')


def test_parse_and_roll_critical():
    crits = [DiceRoller.parse_and_roll('1d20')[4] for _ in range(1000)]
    assert any(crits), '1d20 never produced a critical hit in 1000 rolls'
    print('  parse_and_roll detects critical hits on 1d20')


def test_advantage_vs_disadvantage():
    adv = [DiceRoller.parse_and_roll('1d20', advantage=True)[0] for _ in range(200)]
    assert sum(adv) / 200 > 10.5, 'Advantage average should exceed 10.5'
    print(f'  Advantage avg: {sum(adv)/200:.1f} (expected > 10.5)')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 2 — Game logic helpers
# ═════════════════════════════════════════════════════════════════════════════

def test_ability_modifier():
    cases = [(10, 0), (11, 0), (8, -1), (9, -1), (18, 4), (20, 5), (1, -5), (30, 10)]
    for score, expected in cases:
        got = ability_modifier(score)
        assert got == expected, f'ability_modifier({score}) = {got}, expected {expected}'
    print(f'  ability_modifier correct for {len(cases)} values')


def test_calculate_ac():
    neutral = {'STR':10,'DEX':10,'CON':10,'INT':10,'WIS':10,'CHA':10}
    high_dex = {'STR':10,'DEX':18,'CON':10,'INT':10,'WIS':10,'CHA':10}

    # Fighter: heavy armor (base 16 from game_data) + shield (+2) = 18
    fighter_ac = calculate_ac('Fighter', neutral)
    assert fighter_ac >= 16, f'Fighter AC {fighter_ac} < 16'

    # Wizard: unarmored = 10 + DEX mod = 10 + 4 = 14
    wiz_ac = calculate_ac('Wizard', high_dex)
    assert wiz_ac == 14, f'Wizard AC {wiz_ac}, expected 14'

    # Barbarian: 10 + DEX mod + CON mod
    barb = {'STR':16,'DEX':14,'CON':16,'INT':8,'WIS':12,'CHA':10}
    barb_ac = calculate_ac('Barbarian', barb)
    assert barb_ac == 15, f'Barbarian AC {barb_ac}, expected 15'

    print('  calculate_ac correct for Fighter, Wizard, Barbarian')


def test_calculate_hp():
    # Fighter (d10) + CON +3 = 13
    scores = {'STR':10,'DEX':10,'CON':16,'INT':10,'WIS':10,'CHA':10}
    hp = calculate_hp('Fighter', scores)
    assert hp == 13, f'Fighter HP {hp}, expected 13'

    # Wizard (d6) + CON -1 = 5
    wiz_scores = {'STR':10,'DEX':10,'CON':8,'INT':15,'WIS':12,'CHA':10}
    hp = calculate_hp('Wizard', wiz_scores)
    assert hp == 5, f'Wizard HP {hp}, expected 5'
    print('  calculate_hp correct for Fighter and Wizard')


def test_apply_racial_asi_human():
    base = {'STR':15,'DEX':14,'CON':13,'INT':12,'WIS':10,'CHA':8}
    final = apply_racial_asi(base, 'Human')
    for ab, val in base.items():
        assert final[ab] == val + 1, f'Human {ab}: {final[ab]} != {val+1}'
    print('  apply_racial_asi correct for Human (+1 all)')


def test_apply_racial_asi_half_elf():
    base = {'STR':15,'DEX':14,'CON':13,'INT':12,'WIS':10,'CHA':8}
    final = apply_racial_asi(base, 'Half-Elf', flex1='STR', flex2='DEX')
    assert final['STR'] == 16, f'Half-Elf STR {final["STR"]}, expected 16'
    assert final['DEX'] == 15, f'Half-Elf DEX {final["DEX"]}, expected 15'
    assert final['CHA'] == 10, f'Half-Elf CHA {final["CHA"]}, expected 10 (8+2)'
    print('  apply_racial_asi correct for Half-Elf with flex')


def test_get_spell_slots():
    # Wizard lv1 → 2 level-1 slots
    slots = get_spell_slots('Wizard', level=1)
    assert '1' in slots and slots['1']['max'] == 2

    # Wizard lv3 → 4 level-1, 2 level-2
    slots3 = get_spell_slots('Wizard', level=3)
    assert slots3['1']['max'] == 4 and slots3['2']['max'] == 2

    # Fighter → no slots
    assert get_spell_slots('Fighter', level=1) == {}

    # Warlock lv1 → 1 slot at level 1
    assert get_spell_slots('Warlock', level=1)['1']['max'] == 1

    # Warlock lv3 → slots at level 2
    assert '2' in get_spell_slots('Warlock', level=3)

    print('  get_spell_slots correct for Wizard, Fighter, Warlock')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 3 — Authentication
# ═════════════════════════════════════════════════════════════════════════════

def test_register_success():
    client = make_client()
    r = register(client, 'hero', role='player')
    assert r.status_code == 200
    with flask_app.app_context():
        u = User.query.filter_by(username='hero').first()
        assert u is not None and u.role == 'player'
    print('  Register: player created successfully')


def test_register_duplicate():
    client = make_client()
    register(client, 'hero')
    client.get('/logout')
    register(client, 'hero')  # second attempt
    with flask_app.app_context():
        assert User.query.filter_by(username='hero').count() == 1
    print('  Register: duplicate username rejected')


def test_register_password_mismatch():
    client = make_client()
    client.post('/register', data={
        'username': 'hero', 'password': 'abc', 'confirm': 'xyz', 'role': 'player',
    }, follow_redirects=True)
    with flask_app.app_context():
        assert User.query.filter_by(username='hero').first() is None
    print('  Register: password mismatch rejected')


def test_login_success():
    client = make_client()
    register(client, 'hero', role='player')
    client.get('/logout')
    r = login(client, 'hero')
    assert r.status_code == 200
    print('  Login: correct credentials accepted')


def test_login_bad_password():
    client = make_client()
    register(client, 'hero')
    client.get('/logout')
    r = client.post('/login', data={'username': 'hero', 'password': 'wrong'},
                    follow_redirects=True)
    assert b'Invalid' in r.data
    # Protected routes redirect after bad login
    r2 = client.get('/characters', follow_redirects=False)
    assert r2.status_code == 302
    print('  Login: bad password rejected, protected routes inaccessible')


def test_logout():
    client = make_client()
    register(client, 'hero')
    client.get('/logout')
    r2 = client.get('/characters', follow_redirects=False)
    assert r2.status_code == 302
    print('  Logout: protected routes redirect after logout')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 4 — Character management
# ═════════════════════════════════════════════════════════════════════════════

def test_character_list_requires_auth():
    client = make_client()
    r = client.get('/characters', follow_redirects=False)
    assert r.status_code == 302
    print('  Character list: requires authentication')


def test_character_creation():
    client = make_client()
    register(client, 'hero')
    r = client.post('/characters/new', data=fighter_form(), follow_redirects=True)
    assert r.status_code == 200
    assert b'Arlen' in r.data, 'Character name not found in response'
    assert b'Fighter' in r.data
    # Verify HP/AC > 0 via DB
    with flask_app.app_context():
        char = Character.query.filter_by(name='Arlen').first()
        assert char is not None
        assert char.hp_max > 0 and char.ac > 0
        # Human ASI: base STR 15 + 1 = 16
        assert char.ability_scores['STR'] == 16
    print('  Character creation: Fighter created with correct stats')


def test_character_creation_spellcaster():
    client = make_client()
    register(client, 'mage')
    r = client.post('/characters/new', data=wizard_form(), follow_redirects=True)
    assert r.status_code == 200
    assert b'Elaryn' in r.data
    with flask_app.app_context():
        char = Character.query.filter_by(name='Elaryn').first()
        assert char is not None
        spells = char.spells or {}
        assert spells.get('spellcasting') == 'INT'
        assert spells.get('slots', {}).get('1', {}).get('max') == 2
        assert spells.get('gold', 0) == 10  # Sage gives 10 gp
    print('  Character creation: Wizard has spell slots and starting gold')


def test_character_sheet_view():
    client = make_client()
    register(client, 'hero')
    client.post('/characters/new', data=fighter_form(), follow_redirects=True)
    with flask_app.app_context():
        char = Character.query.filter_by(name='Arlen').first()
        assert char is not None
        cid = char.id
    r = client.get(f'/characters/{cid}')
    assert r.status_code == 200
    assert b'Arlen' in r.data and b'Fighter' in r.data
    print('  Character sheet: renders correctly')


def test_character_creation_invalid():
    client = make_client()
    register(client, 'hero')
    bad = fighter_form()
    bad['name'] = ''  # override name to empty
    r = client.post('/characters/new', data=bad, follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        assert Character.query.filter_by(class_name='Fighter').first() is None
    print('  Character creation: empty name rejected')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 5 — DM campaign management
# ═════════════════════════════════════════════════════════════════════════════

def test_dm_create_campaign():
    client = make_client()
    register(client, 'dm1', role='dm')
    r = client.post('/dm/campaigns/new', data={'name': 'Lost Mine'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'Lost Mine' in r.data
    with flask_app.app_context():
        c = Campaign.query.filter_by(name='Lost Mine').first()
        assert c is not None and len(c.join_code) == 6
    print('  DM: campaign created with 6-char join code')


def test_dm_campaign_page():
    client = make_client()
    register(client, 'dm1', role='dm')
    client.post('/dm/campaigns/new', data={'name': 'Lost Mine'}, follow_redirects=True)
    with flask_app.app_context():
        cid = Campaign.query.filter_by(name='Lost Mine').first().id
    r = client.get(f'/dm/campaigns/{cid}')
    assert r.status_code == 200
    assert b'Lost Mine' in r.data
    print('  DM: campaign detail page renders')


def test_combat_start_and_advance():
    client = make_client()

    # Create DM + campaign
    register(client, 'dm1', role='dm')
    client.post('/dm/campaigns/new', data={'name': 'Test Campaign'}, follow_redirects=True)
    client.get('/logout')

    # Create player + character
    register(client, 'ply1', role='player')
    client.post('/characters/new', data=fighter_form(), follow_redirects=True)

    with flask_app.app_context():
        campaign = Campaign.query.filter_by(name='Test Campaign').first()
        cid, join_code = campaign.id, campaign.join_code

    # Player joins campaign
    client.post('/player/campaigns/join', data={'join_code': join_code},
                follow_redirects=True)
    client.get('/logout')

    # DM starts combat
    login(client, 'dm1')
    r = client.post(f'/dm/campaigns/{cid}/combat/start', follow_redirects=True)
    assert r.status_code == 200

    with flask_app.app_context():
        state = Campaign.query.get(cid).current_state or {}
        assert state.get('combat_active') is True
        assert len(state.get('initiative_order', [])) >= 1

    # Advance turn
    client.post(f'/dm/campaigns/{cid}/combat/next', follow_redirects=True)

    # End combat
    client.post(f'/dm/campaigns/{cid}/combat/end', follow_redirects=True)
    with flask_app.app_context():
        assert Campaign.query.get(cid).current_state.get('combat_active') is False

    print('  Combat: start → next turn → end cycle works')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 6 — Player actions
# ═════════════════════════════════════════════════════════════════════════════

def test_player_join_campaign():
    client = make_client()
    register(client, 'dm1', role='dm')
    client.post('/dm/campaigns/new', data={'name': 'Open Gates'}, follow_redirects=True)
    client.get('/logout')

    with flask_app.app_context():
        c = Campaign.query.filter_by(name='Open Gates').first()
        cid, code = c.id, c.join_code

    register(client, 'ply1', role='player')
    r = client.post('/player/campaigns/join', data={'join_code': code},
                    follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        c = Campaign.query.get(cid)
        uid = User.query.filter_by(username='ply1').first().id
        assert uid in c.players
    print('  Player: join campaign with valid code')


def test_player_dice_roll():
    client = make_client()
    register(client, 'dm1', role='dm')
    client.post('/dm/campaigns/new', data={'name': 'Caves'}, follow_redirects=True)
    client.get('/logout')

    with flask_app.app_context():
        c = Campaign.query.filter_by(name='Caves').first()
        cid, code = c.id, c.join_code

    register(client, 'ply1', role='player')
    client.post('/player/campaigns/join', data={'join_code': code}, follow_redirects=True)
    r = client.post(f'/player/campaigns/{cid}/roll', data={'dice': '1d20'},
                    follow_redirects=True)
    assert r.status_code == 200
    print('  Player: dice roll in campaign accepted')


def test_player_invalid_dice():
    client = make_client()
    register(client, 'dm1', role='dm')
    client.post('/dm/campaigns/new', data={'name': 'Caves2'}, follow_redirects=True)
    client.get('/logout')

    with flask_app.app_context():
        c = Campaign.query.filter_by(name='Caves2').first()
        cid, code = c.id, c.join_code

    register(client, 'ply1', role='player')
    client.post('/player/campaigns/join', data={'join_code': code}, follow_redirects=True)
    r = client.post(f'/player/campaigns/{cid}/roll', data={'dice': 'notadice'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'Invalid' in r.data or b'invalid' in r.data
    print('  Player: invalid dice expression flashes error')


# ═════════════════════════════════════════════════════════════════════════════
# GROUP 7 — Phase 5: Inventory, Gold, Rests, Spells
# ═════════════════════════════════════════════════════════════════════════════

def _setup_char(client, username, form_fn=fighter_form):
    register(client, username)
    form = form_fn()
    char_name = dict(form).get('name') or next(v for k, v in form if k == 'name')
    client.post('/characters/new', data=form, follow_redirects=True)
    with flask_app.app_context():
        char = Character.query.filter_by(name=char_name).first()
        assert char is not None, f'Character {char_name} not found after creation'
        return char.id


def test_inventory_add():
    client = make_client()
    cid = _setup_char(client, 'hero')
    r = client.post(f'/characters/{cid}/inventory/add',
                    data={'item': 'Healing Potion'}, follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        assert 'Healing Potion' in Character.query.get(cid).equipment
    print('  Inventory: item added successfully')


def test_inventory_remove():
    client = make_client()
    cid = _setup_char(client, 'hero')
    client.post(f'/characters/{cid}/inventory/add', data={'item': 'Torch'},
                follow_redirects=True)
    with flask_app.app_context():
        idx = Character.query.get(cid).equipment.index('Torch')
    r = client.post(f'/characters/{cid}/inventory/remove/{idx}', follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        assert 'Torch' not in Character.query.get(cid).equipment
    print('  Inventory: item removed by index')


def test_gold_adjust():
    client = make_client()
    cid = _setup_char(client, 'hero')
    with flask_app.app_context():
        initial = (Character.query.get(cid).spells or {}).get('gold', 0)

    client.post(f'/characters/{cid}/gold', data={'delta': '50'}, follow_redirects=True)
    with flask_app.app_context():
        assert (Character.query.get(cid).spells or {}).get('gold') == initial + 50

    client.post(f'/characters/{cid}/gold', data={'delta': '-20'}, follow_redirects=True)
    with flask_app.app_context():
        assert (Character.query.get(cid).spells or {}).get('gold') == initial + 30

    print(f'  Gold: +50 then -20 from base {initial} = {initial+30}')


def test_gold_cannot_go_negative():
    client = make_client()
    cid = _setup_char(client, 'hero')
    client.post(f'/characters/{cid}/gold', data={'delta': '-9999'}, follow_redirects=True)
    with flask_app.app_context():
        assert (Character.query.get(cid).spells or {}).get('gold', 0) >= 0
    print('  Gold: cannot go below 0')


def test_short_rest():
    client = make_client()
    cid = _setup_char(client, 'hero')
    with flask_app.app_context():
        char = Character.query.get(cid)
        char.hp_current = max(1, char.hp_max - 5)
        db.session.commit()
        before_hd = (char.spells or {}).get('hit_dice_current', 1)

    r = client.post(f'/characters/{cid}/rest/short', data={'num_dice': '1'},
                    follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        after_hd = (Character.query.get(cid).spells or {}).get('hit_dice_current', 0)
        assert after_hd == before_hd - 1
    print('  Short rest: hit die consumed')


def test_short_rest_no_dice():
    client = make_client()
    cid = _setup_char(client, 'hero')
    with flask_app.app_context():
        from sqlalchemy.orm.attributes import flag_modified
        char = Character.query.get(cid)
        extra = dict(char.spells or {})
        extra['hit_dice_current'] = 0
        char.spells = extra
        flag_modified(char, 'spells')
        db.session.commit()

    r = client.post(f'/characters/{cid}/rest/short', data={'num_dice': '1'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'No hit dice' in r.data
    print('  Short rest: blocked when no hit dice remain')


def test_long_rest():
    client = make_client()
    cid = _setup_char(client, 'hero')
    with flask_app.app_context():
        from sqlalchemy.orm.attributes import flag_modified
        char = Character.query.get(cid)
        char.hp_current = 1
        extra = dict(char.spells or {})
        extra['hit_dice_current'] = 0
        char.spells = extra
        flag_modified(char, 'spells')
        db.session.commit()
        max_hp = char.hp_max

    r = client.post(f'/characters/{cid}/rest/long', follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        char = Character.query.get(cid)
        assert char.hp_current == max_hp
        assert (char.spells or {}).get('hit_dice_current', 0) >= 1
    print('  Long rest: HP fully restored, hit dice regained')


def test_spell_cast_consumes_slot():
    client = make_client()
    cid = _setup_char(client, 'mage', form_fn=wizard_form)
    r = client.post(f'/characters/{cid}/cast',
                    data={'slot_level': '1', 'spell_name': 'Magic Missile'},
                    follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        slots = (Character.query.get(cid).spells or {}).get('slots', {})
        assert slots['1']['current'] == 1  # started at 2, now 1
    print('  Spellcasting: slot consumed on cast')


def test_spell_cast_no_slots():
    client = make_client()
    cid = _setup_char(client, 'mage', form_fn=wizard_form)
    # Exhaust both level-1 slots
    client.post(f'/characters/{cid}/cast', data={'slot_level': '1', 'spell_name': 'S1'},
                follow_redirects=True)
    client.post(f'/characters/{cid}/cast', data={'slot_level': '1', 'spell_name': 'S2'},
                follow_redirects=True)
    # Third cast should fail
    r = client.post(f'/characters/{cid}/cast', data={'slot_level': '1', 'spell_name': 'S3'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'No' in r.data
    print('  Spellcasting: blocked when no slots remaining')


def test_concentration():
    client = make_client()
    cid = _setup_char(client, 'mage', form_fn=wizard_form)
    client.post(f'/characters/{cid}/cast',
                data={'slot_level': '1', 'spell_name': 'Bless', 'concentration': 'on'},
                follow_redirects=True)
    with flask_app.app_context():
        assert (Character.query.get(cid).spells or {}).get('concentration') == 'Bless'

    r = client.post(f'/characters/{cid}/concentration/clear', follow_redirects=True)
    assert r.status_code == 200
    with flask_app.app_context():
        assert (Character.query.get(cid).spells or {}).get('concentration') is None
    print('  Concentration: set on cast, cleared on demand')


def test_long_rest_restores_spell_slots():
    client = make_client()
    cid = _setup_char(client, 'mage', form_fn=wizard_form)
    client.post(f'/characters/{cid}/cast', data={'slot_level': '1'}, follow_redirects=True)
    client.post(f'/characters/{cid}/cast', data={'slot_level': '1'}, follow_redirects=True)
    client.post(f'/characters/{cid}/rest/long', follow_redirects=True)
    with flask_app.app_context():
        slots = (Character.query.get(cid).spells or {}).get('slots', {})
        assert slots['1']['current'] == slots['1']['max']
    print('  Long rest: spell slots fully restored')


# ═════════════════════════════════════════════════════════════════════════════
# Runner
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    tests = [
        # Group 1 — DiceRoller
        ('DiceRoller — parse_and_roll valid',    test_parse_and_roll_valid),
        ('DiceRoller — parse_and_roll invalid',  test_parse_and_roll_invalid),
        ('DiceRoller — critical hit detection',  test_parse_and_roll_critical),
        ('DiceRoller — advantage avg > 10.5',    test_advantage_vs_disadvantage),
        # Group 2 — Game logic
        ('Logic — ability_modifier',             test_ability_modifier),
        ('Logic — calculate_ac',                 test_calculate_ac),
        ('Logic — calculate_hp',                 test_calculate_hp),
        ('Logic — racial ASI (Human)',           test_apply_racial_asi_human),
        ('Logic — racial ASI (Half-Elf flex)',   test_apply_racial_asi_half_elf),
        ('Logic — spell slot tables',            test_get_spell_slots),
        # Group 3 — Auth
        ('Auth — register success',              test_register_success),
        ('Auth — register duplicate',            test_register_duplicate),
        ('Auth — register password mismatch',    test_register_password_mismatch),
        ('Auth — login success',                 test_login_success),
        ('Auth — login bad password',            test_login_bad_password),
        ('Auth — logout',                        test_logout),
        # Group 4 — Characters
        ('Character — list requires auth',       test_character_list_requires_auth),
        ('Character — create Fighter',           test_character_creation),
        ('Character — create Wizard',            test_character_creation_spellcaster),
        ('Character — sheet renders',            test_character_sheet_view),
        ('Character — empty name rejected',      test_character_creation_invalid),
        # Group 5 — DM
        ('DM — create campaign',                 test_dm_create_campaign),
        ('DM — campaign page renders',           test_dm_campaign_page),
        ('DM — combat start/next/end',           test_combat_start_and_advance),
        # Group 6 — Player
        ('Player — join campaign',               test_player_join_campaign),
        ('Player — dice roll',                   test_player_dice_roll),
        ('Player — invalid dice error',          test_player_invalid_dice),
        # Group 7 — Phase 5
        ('Inventory — add item',                 test_inventory_add),
        ('Inventory — remove item',              test_inventory_remove),
        ('Gold — add and spend',                 test_gold_adjust),
        ('Gold — cannot go negative',            test_gold_cannot_go_negative),
        ('Rest — short rest consumes hit die',   test_short_rest),
        ('Rest — short rest blocked no dice',    test_short_rest_no_dice),
        ('Rest — long rest restores HP',         test_long_rest),
        ('Spells — cast consumes slot',          test_spell_cast_consumes_slot),
        ('Spells — blocked with no slots',       test_spell_cast_no_slots),
        ('Spells — concentration set/cleared',   test_concentration),
        ('Spells — long rest restores slots',    test_long_rest_restores_spell_slots),
    ]

    passed = failed = 0
    for name, fn in tests:
        print(f'[TEST] {name}')
        try:
            fn()
            print('  PASS')
            passed += 1
        except Exception as e:
            import traceback
            print(f'  FAIL: {e}')
            traceback.print_exc()
            failed += 1

    print(f'\n{"="*50}')
    print(f'Results: {passed}/{passed + failed} tests passed')
    if failed:
        sys.exit(1)
