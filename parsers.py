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


# Known field names within NPC and Chapter blocks (used to delimit multiline values)
_NPC_FIELDS    = ['HP', 'AC', 'Initiative Bonus', 'Notes', 'Scene', 'Dialogue']
_CHAPTER_FIELDS = ['Description', 'Status', 'Notes', 'Branch']


def _multiline_field(body, key, known_fields, default=''):
    """
    Extract a field value that may span multiple lines.

    Captures everything from 'Key: ...' up to the next known field name
    at the start of a line, or end of the block.
    """
    fields_pat = '|'.join(re.escape(f) for f in known_fields)
    pattern = rf'^{re.escape(key)}:\s*(.*?)(?=^(?:{fields_pat})\s*:|\Z)'
    m = re.search(pattern, body, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else default


# ── Character parser ───────────────────────────────────────────────────────────

def parse_character_md(text):
    """
    Parse a character markdown template (v2 format).

    Expected format::

        ## Basic Info
        Name: Thorin Ironforge
        Race: Dwarf
        Class: Fighter
        Background: Soldier
        Alignment: Lawful Good

        ## Ability Scores
        STR: 15  DEX: 10  CON: 14  INT: 13  WIS: 12  CHA: 8

        ## Skill Proficiencies
        - Athletics
        - Perception

        ## Equipment
        - Longsword
        - Shield

        ## Gold
        Gold: 10

        ## Physical Characteristics
        Height: 4'5"
        Weight: 150 lbs
        Age: 58
        Eyes: Steel grey
        Hair: Black, braided
        Skin: Bronzed
        Gender: Male

        ## Backstory
        Born in the mountain holds of Kharak Dûm...

        ## Personality Traits
        I am always polite and respectful, even to my enemies.

        ## Ideals
        Honor. I never break my word, no matter the cost.

        ## Bonds
        I will do anything to protect my clan's legacy.

        ## Flaws
        I am too proud to admit when I am wrong.

        ## Appearance
        A stocky dwarf with a black braided beard reaching his belt...

    Returns a dict with all fields. New in v2:
        physical (dict of height/weight/age/eyes/hair/skin/gender),
        custom_background, personality_traits, ideals, bonds, flaws, appearance (all str)
    """
    basics     = _section(text, 'Basic Info')
    scores_sec = _section(text, 'Ability Scores')
    skills_sec = _section(text, 'Skill Proficiencies')
    equip_sec  = _section(text, 'Equipment')
    gold_sec   = _section(text, 'Gold')
    phys_sec   = _section(text, 'Physical Characteristics')

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
        # Phase 20 background fields
        'physical': {
            'height': _kv(phys_sec, 'Height'),
            'weight': _kv(phys_sec, 'Weight'),
            'age':    _kv(phys_sec, 'Age'),
            'eyes':   _kv(phys_sec, 'Eyes'),
            'hair':   _kv(phys_sec, 'Hair'),
            'skin':   _kv(phys_sec, 'Skin'),
            'gender': _kv(phys_sec, 'Gender'),
        },
        'custom_background':  _section(text, 'Backstory'),
        'personality_traits': _section(text, 'Personality Traits'),
        'ideals':             _section(text, 'Ideals'),
        'bonds':              _section(text, 'Bonds'),
        'flaws':              _section(text, 'Flaws'),
        'appearance':         _section(text, 'Appearance'),
    }


# ── Campaign parser ────────────────────────────────────────────────────────────

def _parse_chapters(text):
    """
    Parse the ## Chapters section of a campaign markdown.

    Each chapter uses:
        ### Chapter: Title
        Description: Multi-line description of this chapter.
        Status: upcoming
        Notes: DM notes for running this chapter.
        Branch: Path A — do this thing
        Branch: Path B — do the other thing

    Returns a list of chapter dicts compatible with the Phase 15 chapter tracker.
    """
    chapters_sec = _section(text, 'Chapters')
    if not chapters_sec:
        return []

    chapters = []
    for m in re.finditer(
        r'^###\s+Chapter:\s+(.+?)\n(.*?)(?=^###\s+Chapter:|\Z)',
        chapters_sec, re.MULTILINE | re.DOTALL
    ):
        title = m.group(1).strip()
        body  = m.group(2)

        description = _multiline_field(body, 'Description', _CHAPTER_FIELDS, '')
        notes       = _multiline_field(body, 'Notes',       _CHAPTER_FIELDS, '')
        status      = _kv(body, 'Status', 'upcoming').lower().strip()
        if status not in ('upcoming', 'active', 'completed'):
            status = 'upcoming'

        branch_names = re.findall(r'^Branch:\s*(.+)$', body, re.MULTILINE)
        branches = [{'name': b.strip(), 'description': ''} for b in branch_names]

        chapters.append({
            'title':         title,
            'description':   description,
            'status':        status,
            'notes':         notes,
            'summary':       '',
            'branches':      branches,
            'active_branch': None,
        })

    return chapters


def parse_campaign_md(text):
    """
    Parse a campaign markdown template (v2 format).

    Expected format::

        ## Campaign Info
        Name: The Lost Mine
        Description: A classic starter adventure.

        ## Opening Narration
        The road stretches out before you...

        ## Chapters
        ### Chapter: Act One
        Description: The party is ambushed on the road.
        Status: upcoming
        Notes: Party should be level 1. Main goal: reach town.
        Branch: Follow the goblins north
        Branch: Push on to town and ask for help

        ## NPCs
        ### Goblin Scout
        HP: 7
        AC: 13
        Initiative Bonus: +2
        Notes: Will flee when below half HP.
        Scene: A pair of goblins lurk behind mossy boulders beside the trail.
        Dialogue: "Yikes! Don't kill Gribble! Gribble talk!"

    Returns a dict:
        name, description, opening_narration (str),
        npc_presets (list of {name, hp, ac, initiative_bonus, notes}),
        chapters (list of chapter dicts)
    """
    info_sec      = _section(text, 'Campaign Info')
    narration_sec = _section(text, 'Opening Narration')

    # Parse NPC blocks — each starts with ### NPC Name
    # Skip blocks inside ## Chapters (those use ### Chapter: prefix)
    npc_presets = []
    npcs_sec = _section(text, 'NPCs')
    for m in re.finditer(
        r'^###\s+(.+?)\n(.*?)(?=^###\s|\Z)', npcs_sec, re.MULTILINE | re.DOTALL
    ):
        name = m.group(1).strip()
        # Skip chapter-divider headers that leaked into NPC section (v1 compat)
        if re.match(r'^-+$', name) or name.upper().startswith('CHAPTER'):
            continue
        body = m.group(2)

        notes    = _multiline_field(body, 'Notes',    _NPC_FIELDS, '')
        scene    = _multiline_field(body, 'Scene',    _NPC_FIELDS, '')
        dialogue = _multiline_field(body, 'Dialogue', _NPC_FIELDS, '')

        # Combine into rich notes for the NPC preset display
        rich_notes = notes
        if scene:
            rich_notes += f'\n\nSCENE: {scene}'
        if dialogue:
            rich_notes += f'\n\nDIALOGUE: {dialogue}'

        npc_presets.append({
            'name':             name,
            'hp':               _safe_int(_kv(body, 'HP', '10'), default=10, lo=1, hi=9999),
            'ac':               _safe_int(_kv(body, 'AC', '12'), default=12, lo=1,  hi=30),
            'initiative_bonus': _safe_int(_kv(body, 'Initiative Bonus', '0'), default=0, lo=-10, hi=20),
            'notes':            rich_notes.strip(),
        })

    return {
        'name':              _kv(info_sec, 'Name', 'Imported Campaign'),
        'description':       _kv(info_sec, 'Description', ''),
        'opening_narration': narration_sec,
        'npc_presets':       npc_presets,
        'chapters':          _parse_chapters(text),
    }


# ── Template strings ───────────────────────────────────────────────────────────

CHARACTER_TEMPLATE = """\
# Character Sheet
# Campaign Codex — Character Import Template (v2)
# Fill in your details below and import via the Characters page.
# Lines starting with # are comments and are ignored.

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

## Physical Characteristics
Height: 5'10"
Weight: 165 lbs
Age: 28
Eyes: Brown
Hair: Dark brown, short
Skin: Tanned
Gender: Male

## Backstory
Write your character's full origin story here. Be as detailed as you like —
this text drives the AI generation for your personality traits, ideals, bonds,
flaws, and appearance on the character sheet.

## Personality Traits
How does your character act day-to-day? What are their mannerisms, quirks,
and habits? What do other people notice about them first?

## Ideals
What principle does your character live by? What drives them forward even
when things are hard? This could be a belief, a cause, or a code of honor.

## Bonds
Who or what does your character care about most? What ties them to the world —
a person, a place, a promise, or a memory they carry with them?

## Flaws
What weakness, vice, or blind spot holds your character back? What might
betray them at the worst possible moment?

## Appearance
Describe what your character looks like — their build, face, distinctive
features, how they dress, and how they carry themselves.
"""

CAMPAIGN_TEMPLATE = """\
# Campaign

## Campaign Info
Name: My Campaign Name
Description: A brief description of the adventure.

## Opening Narration
Write your opening scene description here. This text will appear in the
narration log visible to all players when they load the campaign.

## Chapters
### Chapter: Act One — The Beginning
Description: Set the stage for the adventure. Where does the party start?
  What is their immediate goal? Summarise in a few sentences.
Status: upcoming
Notes: DM notes for running this chapter. Suggested level, key objectives,
  things to remember.
Branch: The direct path — players push forward immediately
Branch: The cautious path — players investigate before committing

### Chapter: Act Two — Rising Conflict
Description: The party discovers the true scope of the threat and faces
  escalating challenges.
Status: upcoming
Notes: Mid-campaign chapter. Introduce complications and NPC alliances.
Branch: Ally with the faction in town
Branch: Go it alone

### Chapter: Act Three — The Climax
Description: Final confrontation with the main antagonist.
Status: upcoming
Notes: Final chapter. Make sure the party is well-rested before this.

## NPCs

### Example Villain
HP: 65
AC: 16
Initiative Bonus: +3
Notes: The main antagonist. Powerful and ruthless. Fights to the death.
Scene: The villain stands at the far end of a torchlit throne room, flanked
  by two guards. Their expression is cold and calculating.
Dialogue: "So. You finally made it. I was beginning to think you wouldn't
  come. That would have been a shame — I've prepared something special for you."

### Friendly NPC
HP: 10
AC: 11
Initiative Bonus: +0
Notes: A helpful townsfolk who can provide information and quest hooks.
Scene: A weathered figure leans against the bar, nursing a drink, watching
  the door with cautious eyes.
Dialogue: "You're not from around here, are you? Sit down. There are things
  you should know about this town before night falls."
"""
