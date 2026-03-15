"""
test_sms.py - Tests for SMS AI DM feature
Covers: engine functions, AI DM intent parsing, SMS webhook, phone registration
Run: python tests/test_sms.py
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app, db
from models import User, Character, Campaign
from werkzeug.security import generate_password_hash


flask_app.config.update({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SECRET_KEY': 'test-only-secret',
})


def make_client():
    client = flask_app.test_client()
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    return client


def setup_campaign():
    """Create a DM, player, character, and campaign for testing."""
    dm = User(username='dm', password_hash=generate_password_hash('dm123'), role='dm')
    player = User(username='alice', password_hash=generate_password_hash('pass123'),
                  role='player', phone_number='+15551234567')
    db.session.add_all([dm, player])
    db.session.flush()

    campaign = Campaign(
        name='Test Campaign', dm_id=dm.id,
        join_code='TEST01', players=[player.id],
        current_state={'sms_enabled': True, 'narration_log': [], 'combat_log': []},
        is_active=True,
    )
    db.session.add(campaign)
    db.session.flush()

    char = Character(
        name='Arlen', race='Human', class_name='Fighter', level=1,
        ability_scores={'STR': 16, 'DEX': 14, 'CON': 14, 'INT': 10, 'WIS': 12, 'CHA': 8},
        hp_max=12, hp_current=12, ac=18, proficiency_bonus=2,
        skills=['Athletics', 'Perception'],
        equipment=['Longsword', 'Shield', 'Chain Mail'],
        spells={'spellcasting': None, 'slots': {}, 'known': [],
                'concentration': None, 'hit_dice_max': 1, 'hit_dice_current': 1,
                'hit_die': 10, 'gold': 15},
        user_id=player.id, campaign_id=campaign.id,
    )
    db.session.add(char)
    db.session.commit()

    return dm, player, campaign, char


# ── Engine Tests ─────────────────────────────────────────────────────────────

class TestEngine(unittest.TestCase):

    def test_resolve_skill_check_proficient(self):
        from services.engine import resolve_skill_check
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            result = resolve_skill_check(char, campaign, 'Athletics')
            self.assertIn('Athletics', result['text'])
            self.assertEqual(result['skill'], 'Athletics')
            self.assertEqual(result['ability'], 'STR')
            self.assertEqual(result['prof_bonus'], 2)  # proficient
            self.assertGreaterEqual(result['total'], 1)

    def test_resolve_skill_check_not_proficient(self):
        from services.engine import resolve_skill_check
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            result = resolve_skill_check(char, campaign, 'Stealth')
            self.assertEqual(result['prof_bonus'], 0)

    def test_resolve_skill_check_invalid(self):
        from services.engine import resolve_skill_check
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            result = resolve_skill_check(char, campaign, 'FakeSkill')
            self.assertIn('error', result)

    def test_resolve_attack(self):
        from services.engine import resolve_attack
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            result = resolve_attack(char, campaign, 'Goblin', 'STR', '1d8', target_ac=13)
            self.assertIn('Attack vs Goblin', result['text'])
            self.assertIn('atk_total', result)
            self.assertIn(result['hit'], [True, False])

    def test_resolve_attack_with_damage(self):
        from services.engine import resolve_attack
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            # Force a hit by setting very low AC
            result = resolve_attack(char, campaign, 'Goblin', 'STR', '1d8', target_ac=1)
            self.assertTrue(result['hit'])
            self.assertIn('damage_total', result)
            self.assertGreater(result['damage_total'], 0)

    def test_resolve_roll(self):
        from services.engine import resolve_roll
        result = resolve_roll('2d6+3')
        self.assertIn('total', result)
        self.assertGreaterEqual(result['total'], 5)  # min: 1+1+3
        self.assertEqual(result['modifier'], 3)

    def test_resolve_roll_invalid(self):
        from services.engine import resolve_roll
        result = resolve_roll('not_a_dice')
        self.assertIn('error', result)

    def test_resolve_saving_throw(self):
        from services.engine import resolve_saving_throw
        client = make_client()
        with flask_app.app_context():
            _, _, _, char = setup_campaign()
            result = resolve_saving_throw(char, 'CON')
            self.assertIn('CON save', result['text'])
            self.assertEqual(result['modifier'], 2)  # CON 14 → +2

    def test_get_character_summary(self):
        from services.engine import get_character_summary
        client = make_client()
        with flask_app.app_context():
            _, _, _, char = setup_campaign()
            summary = get_character_summary(char)
            self.assertIn('Arlen', summary)
            self.assertIn('Fighter', summary)
            self.assertIn('HP 12/12', summary)

    def test_get_combat_state_summary_no_combat(self):
        from services.engine import get_combat_state_summary
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, _ = setup_campaign()
            summary = get_combat_state_summary(campaign)
            self.assertIn('Not in combat', summary)

    def test_apply_damage_to_npc(self):
        from services.engine import apply_damage_to_npc
        from sqlalchemy.orm.attributes import flag_modified
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, _ = setup_campaign()
            state = campaign.current_state or {}
            state['combat_active'] = True
            state['initiative_order'] = [
                {'name': 'Goblin', 'is_npc': True, 'npc_hp': 7, 'npc_hp_max': 7,
                 'npc_ac': 13, 'initiative': 10, 'roll_detail': 'd20(8)+2=10'},
            ]
            campaign.current_state = state
            flag_modified(campaign, 'current_state')
            db.session.commit()
            db.session.refresh(campaign)

            result = apply_damage_to_npc(campaign, 'Goblin', 5)
            self.assertEqual(result['old_hp'], 7)
            self.assertEqual(result['new_hp'], 2)
            self.assertFalse(result['defeated'])

    def test_apply_damage_npc_defeated(self):
        from services.engine import apply_damage_to_npc
        from sqlalchemy.orm.attributes import flag_modified
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, _ = setup_campaign()
            state = campaign.current_state or {}
            state['initiative_order'] = [
                {'name': 'Goblin', 'is_npc': True, 'npc_hp': 3, 'npc_hp_max': 7,
                 'npc_ac': 13, 'initiative': 10, 'roll_detail': 'd20(8)+2=10'},
            ]
            campaign.current_state = state
            flag_modified(campaign, 'current_state')
            db.session.commit()
            db.session.refresh(campaign)

            result = apply_damage_to_npc(campaign, 'Goblin', 10)
            self.assertEqual(result['new_hp'], 0)
            self.assertTrue(result['defeated'])


# ── AI DM Tests (mocked Grok) ───────────────────────────────────────────────

class TestAIDM(unittest.TestCase):

    @patch('services.ai_dm._call')
    def test_interpret_attack(self, mock_call):
        mock_call.return_value = (
            '{"action_type": "attack", "params": {"target": "Goblin", "ability": "STR", "damage_dice": "1d8"}, "narration_context": "swinging sword"}',
            None
        )
        from services.ai_dm import interpret_action
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            action, error = interpret_action("I attack the goblin", char, campaign)
            self.assertIsNone(error)
            self.assertEqual(action['action_type'], 'attack')
            self.assertEqual(action['params']['target'], 'Goblin')

    @patch('services.ai_dm._call')
    def test_interpret_skill_check(self, mock_call):
        mock_call.return_value = (
            '{"action_type": "skill_check", "params": {"skill": "Perception"}, "narration_context": "looking around"}',
            None
        )
        from services.ai_dm import interpret_action
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            action, error = interpret_action("I look around the room", char, campaign)
            self.assertIsNone(error)
            self.assertEqual(action['action_type'], 'skill_check')

    @patch('services.ai_dm._call')
    def test_interpret_invalid_json_fallback(self, mock_call):
        mock_call.return_value = ('this is not json at all', None)
        from services.ai_dm import interpret_action
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            action, error = interpret_action("I do something", char, campaign)
            self.assertIsNone(error)
            self.assertEqual(action['action_type'], 'roleplay')

    @patch('services.ai_dm._call')
    def test_interpret_api_error(self, mock_call):
        mock_call.return_value = (None, 'API timeout')
        from services.ai_dm import interpret_action
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            action, error = interpret_action("I do something", char, campaign)
            self.assertIsNotNone(error)

    @patch('services.ai_dm._call')
    def test_narrate_result(self, mock_call):
        mock_call.return_value = ('Your blade bites deep into the goblin.', None)
        from services.ai_dm import narrate_result
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            result = {'text': 'Attack vs Goblin: 18 HIT, 6 dmg'}
            narration, error = narrate_result('attack', {}, result, char, campaign)
            self.assertIsNone(error)
            self.assertIn('goblin', narration.lower())


# ── SMS Webhook Tests ────────────────────────────────────────────────────────

class TestSMSWebhook(unittest.TestCase):

    @patch('services.ai_dm.process_player_sms')
    @patch('services.sms.validate_webhook', return_value=True)
    def test_webhook_valid_player(self, mock_validate, mock_process):
        mock_process.return_value = '[Perception 18] You spot a tripwire.'
        client = make_client()
        with flask_app.app_context():
            setup_campaign()
            resp = client.post('/sms/webhook', data={
                'From': '+15551234567',
                'Body': 'I search the room',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'tripwire', resp.data)
            mock_process.assert_called_once()

    @patch('services.sms.validate_webhook', return_value=True)
    def test_webhook_unknown_phone(self, mock_validate):
        client = make_client()
        with flask_app.app_context():
            setup_campaign()
            resp = client.post('/sms/webhook', data={
                'From': '+19999999999',
                'Body': 'hello',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'not linked', resp.data)

    @patch('services.sms.validate_webhook', return_value=True)
    def test_webhook_sms_disabled(self, mock_validate):
        client = make_client()
        with flask_app.app_context():
            from sqlalchemy.orm.attributes import flag_modified
            _, _, campaign, _ = setup_campaign()
            state = campaign.current_state or {}
            state['sms_enabled'] = False
            campaign.current_state = state
            flag_modified(campaign, 'current_state')
            db.session.commit()

            resp = client.post('/sms/webhook', data={
                'From': '+15551234567',
                'Body': 'I search the room',
            })
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'No active SMS campaign', resp.data)

    @patch('services.sms.validate_webhook', return_value=False)
    def test_webhook_invalid_signature(self, mock_validate):
        client = make_client()
        resp = client.post('/sms/webhook', data={
            'From': '+15551234567',
            'Body': 'hello',
        })
        self.assertEqual(resp.status_code, 403)


# ── Phone Registration Tests ─────────────────────────────────────────────────

class TestPhoneRegistration(unittest.TestCase):

    def test_register_phone(self):
        client = make_client()
        with flask_app.app_context():
            dm, player, campaign, _ = setup_campaign()
            # Remove player's existing phone to test registration
            player.phone_number = None
            db.session.commit()

            # Login as DM
            client.post('/login', data={'username': 'dm', 'password': 'dm123'})

            resp = client.post('/sms/register', data={
                'user_id': player.id,
                'phone_number': '+15559876543',
                'campaign_id': campaign.id,
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            # Verify phone was saved
            updated = User.query.get(player.id)
            self.assertEqual(updated.phone_number, '+15559876543')

    def test_register_phone_normalizes(self):
        client = make_client()
        with flask_app.app_context():
            dm, player, campaign, _ = setup_campaign()
            player.phone_number = None
            db.session.commit()

            client.post('/login', data={'username': 'dm', 'password': 'dm123'})

            resp = client.post('/sms/register', data={
                'user_id': player.id,
                'phone_number': '(555) 987-6543',
                'campaign_id': campaign.id,
            }, follow_redirects=True)

            updated = User.query.get(player.id)
            self.assertEqual(updated.phone_number, '+15559876543')


# ── SMS Toggle Tests ─────────────────────────────────────────────────────────

class TestSMSToggle(unittest.TestCase):

    def test_toggle_sms_on(self):
        client = make_client()
        with flask_app.app_context():
            from sqlalchemy.orm.attributes import flag_modified
            dm, _, campaign, _ = setup_campaign()
            state = campaign.current_state or {}
            state['sms_enabled'] = False
            campaign.current_state = state
            flag_modified(campaign, 'current_state')
            db.session.commit()

            client.post('/login', data={'username': 'dm', 'password': 'dm123'})

            resp = client.post('/sms/toggle', data={
                'campaign_id': campaign.id,
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            db.session.expire_all()
            updated = Campaign.query.get(campaign.id)
            self.assertTrue(updated.current_state.get('sms_enabled'))

    def test_toggle_sms_off(self):
        client = make_client()
        with flask_app.app_context():
            dm, _, campaign, _ = setup_campaign()

            client.post('/login', data={'username': 'dm', 'password': 'dm123'})

            resp = client.post('/sms/toggle', data={
                'campaign_id': campaign.id,
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            updated = Campaign.query.get(campaign.id)
            self.assertFalse(updated.current_state.get('sms_enabled'))


# ── Full Pipeline Test (mocked Grok) ─────────────────────────────────────────

class TestFullPipeline(unittest.TestCase):

    @patch('services.ai_dm._call')
    def test_full_skill_check_pipeline(self, mock_call):
        """Test interpret → resolve → narrate for a skill check."""
        mock_call.side_effect = [
            # First call: interpret
            ('{"action_type": "skill_check", "params": {"skill": "Perception"}, "narration_context": "searching"}', None),
            # Second call: narrate
            ('You scan the room carefully, spotting claw marks on the far wall.', None),
        ]

        from services.ai_dm import process_player_sms
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            response = process_player_sms("I search the room", char, campaign)
            self.assertIn('Perception', response)
            self.assertIn('claw marks', response)

    @patch('services.ai_dm._call')
    def test_full_roleplay_pipeline(self, mock_call):
        """Test roleplay action (no mechanics, just narration)."""
        mock_call.side_effect = [
            ('{"action_type": "roleplay", "params": {}, "narration_context": "talking to the innkeeper"}', None),
            ('The innkeeper eyes you warily. "What do you want?"', None),
        ]

        from services.ai_dm import process_player_sms
        client = make_client()
        with flask_app.app_context():
            _, _, campaign, char = setup_campaign()
            response = process_player_sms("I talk to the innkeeper", char, campaign)
            self.assertIn('innkeeper', response.lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
