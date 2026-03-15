from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey, DateTime
import random
import re

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(10), default='player')  # 'dm' or 'player'
    last_seen = Column(DateTime, nullable=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    discord_id = Column(String(30), unique=True, nullable=True)


class Character(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    race = Column(String(50))
    class_name = Column(String(50))
    level = Column(Integer, default=1)
    ability_scores = Column(JSON)   # {"STR": 15, "DEX": 14, ...}
    hp_max = Column(Integer)
    hp_current = Column(Integer)
    ac = Column(Integer)
    proficiency_bonus = Column(Integer, default=2)
    skills = Column(JSON)           # list of proficient skill names
    equipment = Column(JSON)        # list of item strings
    spells = Column(JSON)           # spell slots / known spells (Phase 5)
    background = Column(String(50))
    alignment = Column(String(30))
    campaign_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)


class Campaign(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    dm_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    join_code = Column(String(10), unique=True)
    players = Column(JSON, default=list)    # list of user IDs
    npcs = Column(JSON, default=list)       # list of NPC character IDs
    current_state = Column(JSON, default=dict)  # {initiative_order, active_conditions, narration_log}
    is_active = Column(Boolean, default=True)


class DiceRoller:
    @staticmethod
    def roll(dice_str, modifier=0, advantage=False, disadvantage=False):
        """
        Roll dice from a string like '1d20', '2d6', etc.
        Returns (total, rolls, is_critical).
        """
        num, die = dice_str.lower().split('d')
        num = int(num)
        die = int(die)

        if advantage and disadvantage:
            rolls = [random.randint(1, die) for _ in range(num)]
        elif advantage:
            rolls = [max(random.randint(1, die), random.randint(1, die)) for _ in range(num)]
        elif disadvantage:
            rolls = [min(random.randint(1, die), random.randint(1, die)) for _ in range(num)]
        else:
            rolls = [random.randint(1, die) for _ in range(num)]

        total = sum(rolls) + modifier
        is_critical = (num == 1 and die == 20 and rolls[0] == 20)
        return total, rolls, is_critical

    @staticmethod
    def parse_and_roll(roll_str, advantage=False, disadvantage=False):
        """
        Parse and roll expressions like '1d20', '2d6+3', 'd8-1'.
        Returns (total, label, rolls, modifier, is_critical).
        Raises ValueError on invalid input.
        """
        s = roll_str.lower().strip().replace(' ', '')
        if s.startswith('d'):
            s = '1' + s
        match = re.match(r'^(\d+)d(\d+)([+-]\d+)?$', s)
        if not match:
            raise ValueError(f'Invalid dice expression: "{roll_str}"')
        num = int(match.group(1))
        die = int(match.group(2))
        mod = int(match.group(3)) if match.group(3) else 0
        if num < 1 or num > 100 or die < 2 or die > 100:
            raise ValueError('Dice out of range (1–100 dice, d2–d100).')
        total, rolls, is_crit = DiceRoller.roll(f'{num}d{die}', modifier=mod,
                                                  advantage=advantage,
                                                  disadvantage=disadvantage)
        mod_str = (f'+{mod}' if mod > 0 else str(mod)) if mod != 0 else ''
        label = f'{num}d{die}{mod_str}'
        return total, label, rolls, mod, is_crit
