import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import DiceRoller, Character, Campaign, db
from app import app


def test_dice_roller_basic():
    result, rolls, is_crit = DiceRoller.roll('1d6')
    assert 1 <= result <= 6, f"1d6 result {result} out of range"
    assert len(rolls) == 1
    assert not is_crit
    print(f"  1d6: rolled {rolls}, total {result}")

def test_dice_roller_multi():
    result, rolls, is_crit = DiceRoller.roll('2d6', modifier=3)
    assert 5 <= result <= 15, f"2d6+3 result {result} out of range"
    assert len(rolls) == 2
    print(f"  2d6+3: rolled {rolls}, total {result}")

def test_dice_roller_d20():
    result, rolls, is_crit = DiceRoller.roll('1d20')
    assert 1 <= result <= 20
    if rolls[0] == 20:
        assert is_crit
    print(f"  1d20: rolled {rolls}, critical={is_crit}")

def test_dice_roller_advantage():
    # Run many times to statistically verify advantage favors higher rolls
    results = [DiceRoller.roll('1d20', advantage=True)[0] for _ in range(100)]
    avg = sum(results) / len(results)
    assert avg > 10.5, f"Advantage average {avg:.1f} should be > 10.5"
    print(f"  Advantage 1d20 average over 100 rolls: {avg:.1f}")

def test_dice_roller_disadvantage():
    results = [DiceRoller.roll('1d20', disadvantage=True)[0] for _ in range(100)]
    avg = sum(results) / len(results)
    assert avg < 10.5, f"Disadvantage average {avg:.1f} should be < 10.5"
    print(f"  Disadvantage 1d20 average over 100 rolls: {avg:.1f}")

def test_dice_roller_cancel():
    # Advantage + disadvantage cancels out
    result, rolls, _ = DiceRoller.roll('1d6', advantage=True, disadvantage=True)
    assert len(rolls) == 1  # No double-rolling
    print(f"  Advantage+Disadvantage cancelled: {rolls}")

def test_model_creation():
    with app.app_context():
        db.create_all()

        char = Character(
            name="Thorin",
            race="Dwarf",
            class_name="Fighter",
            level=1,
            ability_scores={"STR": 16, "DEX": 12, "CON": 15, "INT": 10, "WIS": 13, "CHA": 8},
            hp_max=12,
            hp_current=12,
            ac=16,
            proficiency_bonus=2,
            skills=["Athletics", "Perception"],
            equipment=["Longsword", "Shield", "Chain Mail"],
            spells={}
        )
        db.session.add(char)
        db.session.commit()

        fetched = Character.query.filter_by(name="Thorin").first()
        assert fetched is not None
        assert fetched.race == "Dwarf"
        assert fetched.ability_scores["STR"] == 16
        print(f"  Created and retrieved character: {fetched.name} ({fetched.race} {fetched.class_name})")

        # Cleanup
        db.session.delete(fetched)
        db.session.commit()

def test_campaign_creation():
    with app.app_context():
        db.create_all()

        campaign = Campaign(
            name="Curse of Strahd",
            dm_id="dm_user",
            players=["player1", "player2"],
            npcs=[],
            current_state={"initiative_order": [], "active_conditions": {}}
        )
        db.session.add(campaign)
        db.session.commit()

        fetched = Campaign.query.filter_by(name="Curse of Strahd").first()
        assert fetched is not None
        assert fetched.dm_id == "dm_user"
        assert len(fetched.players) == 2
        print(f"  Created and retrieved campaign: {fetched.name} (DM: {fetched.dm_id})")

        db.session.delete(fetched)
        db.session.commit()


if __name__ == '__main__':
    tests = [
        ("DiceRoller - basic 1d6", test_dice_roller_basic),
        ("DiceRoller - 2d6+3", test_dice_roller_multi),
        ("DiceRoller - d20 critical", test_dice_roller_d20),
        ("DiceRoller - advantage", test_dice_roller_advantage),
        ("DiceRoller - disadvantage", test_dice_roller_disadvantage),
        ("DiceRoller - adv+disadv cancel", test_dice_roller_cancel),
        ("Model - Character creation", test_model_creation),
        ("Model - Campaign creation", test_campaign_creation),
    ]

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            print(f"[TEST] {name}")
            test_fn()
            print(f"  PASS")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed}/{passed+failed} tests passed")
    if failed:
        sys.exit(1)
