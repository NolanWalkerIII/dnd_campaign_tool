"""
seed.py — Populate the database with sample data for playtesting.

Creates:
  DM account     : dm / dm123
  Player 1       : alice / pass123  (Fighter)
  Player 2       : bob / pass123    (Wizard)
  Campaign       : "Lost Mine of Phandelver" — alice and bob joined

Run once after a fresh database:
    python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, calculate_ac, calculate_hp, apply_racial_asi
from models import User, Character, Campaign
from game_data import CLASSES, get_spell_slots
from werkzeug.security import generate_password_hash
import random
import string


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def make_user(username, password, role):
    u = User(username=username,
             password_hash=generate_password_hash(password),
             role=role)
    db.session.add(u)
    db.session.flush()  # get u.id before commit
    return u


def make_fighter(user_id, name='Arlen Stormfist'):
    scores_base = {'STR': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8}
    # Human +1 all
    scores = apply_racial_asi(scores_base, 'Human')
    hp = calculate_hp('Fighter', scores)
    ac = calculate_ac('Fighter', scores)
    hit_die = CLASSES['Fighter']['hit_die']
    char = Character(
        name=name, race='Human', class_name='Fighter', level=1,
        ability_scores=scores,
        hp_max=hp, hp_current=hp, ac=ac, proficiency_bonus=2,
        skills=['Athletics', 'Intimidation', 'Perception'],
        equipment=['Longsword', 'Shield', 'Chain Mail', 'Handaxe x2',
                   'Explorer\'s Pack', 'Insignia of Rank', 'Trophy from Enemy'],
        spells={
            'spellcasting': None,
            'slots': {},
            'known': [],
            'concentration': None,
            'hit_dice_max': 1,
            'hit_dice_current': 1,
            'hit_die': hit_die,
            'gold': 10,
        },
        background='Soldier', alignment='Lawful Good',
        user_id=user_id,
    )
    db.session.add(char)
    db.session.flush()
    return char


def make_wizard(user_id, name='Elaryn Dawnwhisper'):
    scores_base = {'STR': 8, 'DEX': 14, 'CON': 13, 'INT': 15, 'WIS': 12, 'CHA': 10}
    scores = apply_racial_asi(scores_base, 'Human')
    hp = calculate_hp('Wizard', scores)
    ac = calculate_ac('Wizard', scores)
    hit_die = CLASSES['Wizard']['hit_die']
    char = Character(
        name=name, race='Human', class_name='Wizard', level=1,
        ability_scores=scores,
        hp_max=hp, hp_current=hp, ac=ac, proficiency_bonus=2,
        skills=['Arcana', 'History', 'Insight', 'Medicine'],
        equipment=['Spellbook', 'Arcane Focus', 'Scholar\'s Pack',
                   'Bottle of Black Ink', 'Quill', 'Common Clothes'],
        spells={
            'spellcasting': 'INT',
            'slots': get_spell_slots('Wizard', level=1),
            'known': ['Magic Missile', 'Shield', 'Detect Magic', 'Mage Armor'],
            'concentration': None,
            'hit_dice_max': 1,
            'hit_dice_current': 1,
            'hit_die': hit_die,
            'gold': 10,
        },
        background='Sage', alignment='Neutral Good',
        user_id=user_id,
    )
    db.session.add(char)
    db.session.flush()
    return char


def main():
    with app.app_context():
        db.create_all()

        # Check for existing seed data
        if User.query.filter_by(username='dm').first():
            print('Seed data already exists. Delete instance/dnd.db and re-run to reset.')
            return

        print('Seeding database...')

        dm    = make_user('dm',    'dm123',   'dm')
        alice = make_user('alice', 'pass123', 'player')
        bob   = make_user('bob',   'pass123', 'player')

        fighter = make_fighter(alice.id, 'Arlen Stormfist')
        wizard  = make_wizard(bob.id,   'Elaryn Dawnwhisper')

        campaign = Campaign(
            name='Lost Mine of Phandelver',
            dm_id=dm.id,
            join_code=generate_code(),
            players=[alice.id, bob.id],
            npcs=[],
            current_state={
                'initiative_order': [],
                'active_conditions': {},
                'narration_log': [{
                    'text': ('You stand at the entrance of a crumbling mine. '
                             'The smell of damp earth and something sulfurous fills the air. '
                             'Torchlight flickers from somewhere deep within.'),
                    'timestamp': 'Session 1',
                }],
                'combat_log': [],
            },
            is_active=True,
        )
        db.session.add(campaign)
        db.session.commit()

        print(f'''
Done! Sample data created:

  Accounts
  --------
  DM      : dm / dm123
  Player 1: alice / pass123  → {fighter.name} (Lv1 Human Fighter, {fighter.hp_max} HP, AC {fighter.ac})
  Player 2: bob / pass123    → {wizard.name} (Lv1 Human Wizard, {wizard.hp_max} HP, AC {wizard.ac})

  Campaign
  --------
  Name     : {campaign.name}
  Join Code: {campaign.join_code}

Start the app with:
    python app.py
Then open http://localhost:5000
''')


if __name__ == '__main__':
    main()
