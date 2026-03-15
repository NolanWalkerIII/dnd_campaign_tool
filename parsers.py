"""
Markdown parsers for character sheet and campaign import/export.

Both formats use human-readable ## Section headers with Key: Value lines
so users can edit them in any text editor before importing.
"""
import re


# ── Low-level helpers ──────────────────────────────────────────────────────────

def _kv(text, key, default=''):
    """Extract the first 'Key: value' line from text (case-insensitive)."""
    m = re.search(rf'^{re.escape(key)}:\s*(.+)$', text, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else default


def _section(text, header):
    """Return everything between '## Header' and the next '##' (or end of string)."""
    m = re.search(
        rf'^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s|\Z)',
        text, re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return m.group(1).strip() if m else ''


def _list_items(section_text):
    """Return all '- Item' / '* Item' bullet lines from a section block."""
    return [m.group(1).strip()
            for m in re.finditer(r'^[-*]\s+(.+)$', section_text, re.MULTILINE)]


def _safe_int(s, default=8, lo=1, hi=30):
    """Parse an integer, stripping leading '+', clamped to [lo, hi]."""
    try:
        return max(lo, min(hi, int(str(s).strip().replace('+', ''))))
    except (ValueError, TypeError):
        return default


# ── Character parser ───────────────────────────────────────────────────────────

def parse_character_md(text):
    """
    Parse a character markdown template.

    Expected format::

        ## Basic Info
        Name: Thorin Ironforge
        Race: Dwarf
        Class: Fighter
        Background: Soldier
        Alignment: Lawful Good

        ## Ability Scores
        STR: 15
        DEX: 10
        CON: 14
        INT: 13
        WIS: 12
        CHA: 8

        ## Skill Proficiencies
        - Athletics
        - Perception

        ## Equipment
        - Longsword
        - Shield

        ## Gold
        Gold: 10

    Returns a dict:
        name, race, class_name, background, alignment,
        STR/DEX/CON/INT/WIS/CHA (ints, 1-30),
        skills (list of str), equipment_extra (list of str), gold (int >=0)
    """
    basics     = _section(text, 'Basic Info')
    scores_sec = _section(text, 'Ability Scores')
    skills_sec = _section(text, 'Skill Proficiencies')
    equip_sec  = _section(text, 'Equipment')
    gold_sec   = _section(text, 'Gold')

    return {
        'name':            _kv(basics, 'Name'),
        'race':            _kv(basics, 'Race'),
        'class_name':      _kv(basics, 'Class'),
        'background':      _kv(basics, 'Background'),
        'alignment':       _kv(basics, 'Alignment', 'True Neutral'),
        'STR':             _safe_int(_kv(scores_sec, 'STR', '8')),
        'DEX':             _safe_int(_kv(scores_sec, 'DEX', '8')),
        'CON':             _safe_int(_kv(scores_sec, 'CON', '8')),
        'INT':             _safe_int(_kv(scores_sec, 'INT', '8')),
        'WIS':             _safe_int(_kv(scores_sec, 'WIS', '8')),
        'CHA':             _safe_int(_kv(scores_sec, 'CHA', '8')),
        'skills':          _list_items(skills_sec),
        'equipment_extra': _list_items(equip_sec),
        'gold':            _safe_int(_kv(gold_sec, 'Gold', '0'), default=0, lo=0, hi=999999),
    }


# ── Campaign parser ────────────────────────────────────────────────────────────

def parse_campaign_md(text):
    """
    Parse a campaign markdown template.

    Expected format::

        ## Campaign Info
        Name: The Lost Mine
        Description: A classic starter adventure.

        ## Opening Narration
        The road stretches out before you...

        ## NPCs
        ### Goblin Scout
        HP: 7
        AC: 13
        Initiative Bonus: +2
        Notes: Will flee when below half HP.

    Returns a dict:
        name, description, opening_narration (str),
        npc_presets (list of {name, hp, ac, initiative_bonus, notes})
    """
    info_sec      = _section(text, 'Campaign Info')
    narration_sec = _section(text, 'Opening Narration')

    # Each NPC block starts with ### NPC Name
    npc_presets = []
    for m in re.finditer(
        r'^###\s+(.+?)\n(.*?)(?=^###\s|\Z)', text, re.MULTILINE | re.DOTALL
    ):
        name = m.group(1).strip()
        body = m.group(2)
        npc_presets.append({
            'name':             name,
            'hp':               _safe_int(_kv(body, 'HP', '10'), default=10, lo=1, hi=9999),
            'ac':               _safe_int(_kv(body, 'AC', '12'), default=12, lo=1,  hi=30),
            'initiative_bonus': _safe_int(_kv(body, 'Initiative Bonus', '0'), default=0, lo=-10, hi=20),
            'notes':            _kv(body, 'Notes', ''),
        })

    return {
        'name':              _kv(info_sec, 'Name', 'Imported Campaign'),
        'description':       _kv(info_sec, 'Description', ''),
        'opening_narration': narration_sec,
        'npc_presets':       npc_presets,
    }


# ── Template strings ───────────────────────────────────────────────────────────

CHARACTER_TEMPLATE = """\
# Character Sheet

## Basic Info
Name: Your Character Name
Race: Human
Class: Fighter
Background: Soldier
Alignment: True Neutral

## Ability Scores
STR: 15
DEX: 14
CON: 13
INT: 12
WIS: 10
CHA: 8

## Skill Proficiencies
- Athletics
- Perception

## Equipment
- Longsword
- Shield
- Backpack
- Rations (5 days)

## Gold
Gold: 10
"""

CAMPAIGN_TEMPLATE = """\
# Campaign

## Campaign Info
Name: My Campaign Name
Description: A brief description of the adventure.

## Opening Narration
Write your opening scene description here. This text will appear in the
Scene section visible to all players when they load the campaign.

## NPCs
### Example Enemy
HP: 20
AC: 13
Initiative Bonus: +1
Notes: A simple foe. Describe their tactics here.

### Boss Monster
HP: 65
AC: 16
Initiative Bonus: +3
Notes: The main antagonist. Powerful and ruthless.
"""
