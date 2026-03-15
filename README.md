# D&D Campaign Manager

A web-based Dungeons & Dragons 5e campaign management tool. The Dungeon Master runs campaigns from a dedicated interface while players join and interact from their own browser windows — all in real time via a shared Flask server.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask 3.1 |
| ORM | SQLAlchemy 2.0 + Flask-SQLAlchemy 3.1 |
| Database | SQLite (file: `instance/dnd.db`) |
| Frontend | HTML/CSS/JavaScript (Jinja2 templates, no heavy frameworks) |
| Deployment | Docker + docker-compose |

---

## Running the App

### Option A — Local (virtualenv)

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
flask run
# App is available at http://localhost:5000
```

### Option B — Docker

```bash
docker compose up --build
# App is available at http://localhost:5001
```

The SQLite database is persisted in `./instance/` via a volume mount, so data survives container restarts.

---

## Seeding Sample Data

After starting the server, run the seed script to create demo users and a ready-to-play campaign:

```bash
python seed.py
```

This creates:

| Username | Password | Role |
|----------|----------|------|
| `dm` | `dm123` | Dungeon Master |
| `alice` | `pass123` | Player (Fighter: Arlen Stormfist) |
| `bob` | `pass123` | Player (Wizard: Elaryn Dawnwhisper) |

And a campaign called **"Lost Mine of Phandelver"** with both players already joined and an opening narration set.

---

## Running Tests

```bash
python test_suite.py
```

38 tests covering:
- Dice rolling (expressions, advantage/disadvantage, modifiers)
- Game logic (initiative, attack resolution, conditions, death saves)
- Authentication (register, login, logout, role enforcement)
- Character CRUD (creation, stat calculation, equipment, gold)
- DM workflows (campaign creation, player management, narration, NPC management)
- Player workflows (join campaign, skill checks, attack rolls, combat)
- Phase 5 features (spell slots, casting, concentration, short/long rests, inventory)

---

## User Roles

### Dungeon Master (DM)
- Register with role **DM** at `/register`
- One account acts as DM per campaign
- Full access to all character sheets (read + edit)
- Can adjust any character's HP directly
- Sees which players are currently online (active within 5 minutes)
- Can impersonate any player to see exactly what they see (read-only — no actions)

### Player
- Register with role **Player** at `/register`
- Can create and manage their own characters
- Joins campaigns via a campaign code provided by the DM
- Actions are scoped to their own characters

---

## Feature Overview

### Characters

- **Creation wizard** — select race (with ASI bonuses), class, background, alignment, ability scores (standard array), and skill proficiencies
- **Character sheet** — full stat block: ability scores + modifiers, proficiency bonus, AC, speed, saving throws, skills, HP tracker
- **Equipment & Gold** — add/remove inventory items, adjust gold with ± form
- **Spell Slots** — visual filled/empty slot indicators per spell level (auto-populated based on class/level); spellcasters only
- **Hit Dice** — visual tracker; spend during short rests

Supported races: Human, Elf, Dwarf, Halfling, Gnome, Half-Elf, Half-Orc, Tiefling, Dragonborn

Supported classes: Fighter, Wizard, Rogue, Cleric, Ranger, Paladin, Bard, Druid, Warlock, Sorcerer, Monk, Barbarian

### Campaigns

- DM creates a campaign and shares its join code with players
- Players join from their dashboard using the code
- Campaign page auto-refreshes every 20 seconds (pauses while a form field is focused)

### Markdown Import / Export

#### Characters

- **⬇ Download Template** button at the top of the character creation page delivers a pre-filled `character_template.md`
- **Import Character** — upload a filled-in `.md` file to create a character instantly, skipping the form
- Imported ability scores are accepted as-is (not restricted to the standard array), making it easy to bring in existing characters
- Class and background starting equipment + gold are added on top of anything in the file

Character template sections: `## Basic Info`, `## Ability Scores`, `## Skill Proficiencies`, `## Equipment`, `## Gold`

#### Campaigns

- **⬇ Download Template** button in the DM dashboard's "Import Campaign" section delivers `campaign_template.md`
- **Import Campaign** — upload a filled-in `.md` file to create a campaign with the opening narration pre-loaded and NPC presets ready to use
- NPC presets appear in a **📋 Imported NPC Presets** card on the DM campaign page; each preset has a one-click **⚔ Add to Combat** button that populates the combat initiative list with the preset's stats (HP, AC, initiative bonus)

Campaign template sections: `## Campaign Info`, `## Opening Narration`, `## NPCs` (each NPC as a `### Name` block with `HP:`, `AC:`, `Initiative Bonus:`, `Notes:` fields)

### DM Visibility & Player Impersonation

- **Who's Online** panel on the DM dashboard shows every player active in the last 5 minutes, with their character name and current HP
- **👁 View As** buttons appear next to each player in both the Who's Online panel and the Players list inside each campaign
- Clicking "View As" opens the campaign from that player's exact perspective — correct character list, initiative highlighting, and "your turn" banner
- A persistent banner across the top of every page shows "DM View: Viewing as [player] — actions are disabled" with an **Exit View** link
- All player action routes (roll, attack, skill check, cast spell) are blocked during impersonation — the DM cannot accidentally submit actions on a player's behalf

### Narration

- DM types scene narration; it appears in all player views under **Scene**
- Players see the latest narration prominently, with older entries collapsible

### Combat

- **Initiative**: DM rolls for all participants (players + NPCs); order is sorted and displayed
- **Turn management**: Current turn highlighted with ⚡; players see a banner when it's their turn
- **Attack rolls**: Roll to-hit against optional target AC; damage dice resolved server-side; crits auto-double dice
- **Health tracking**: Damage applied to targets; death saves tracked when HP hits 0; conditions (Poisoned, Blinded, etc.) applied by DM
- **Combat log**: Timestamped log of all actions visible to everyone

### Skill Checks

Players can roll any skill check from their campaign page; result is posted to the combat log.

### Spellcasting

- Cast a spell by name, slot level, and optional concentration flag
- Slot is consumed on cast; concentration replaces any existing concentration spell
- DM can end concentration on any character

### Rests

- **Short Rest**: Spend hit dice to recover HP (rolls hit die + CON modifier per die)
- **Long Rest**: Fully restores HP, resets all spell slots and hit dice

### Free Dice Rolls

Any dice expression accepted at any time: `1d20`, `2d6+3`, `d8`, `4d6kh3`, etc.

---

## Project Structure

```
.
├── app.py                  # Flask application, routes, game logic
├── models.py               # SQLAlchemy models (User, Character, Campaign)
├── parsers.py              # Markdown parsers + template strings for import/export
├── seed.py                 # Sample data for demo/playtesting
├── test_suite.py           # 38-test automated test suite
├── requirements.txt        # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── instance/
│   └── dnd.db              # SQLite database (created at runtime)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── character_sheet.html
│   ├── character_new.html
│   ├── dm/
│   │   ├── dashboard.html
│   │   ├── campaign.html
│   │   └── campaign_new.html
│   └── player/
│       ├── dashboard.html
│       └── campaign.html
└── Documentation/          # D&D 5e reference docs used during development
    ├── 00_INDEX.md
    ├── 01_CORE_MECHANICS.md
    ├── 02_CHARACTER_CREATION.md
    ├── 03_CLASSES_REFERENCE.md
    ├── 04_RACES_REFERENCE.md
    ├── 05_COMBAT.md
    ├── 06_SPELLCASTING.md
    ├── 07_SPELLS_REFERENCE.md
    ├── 08_CONDITIONS.md
    ├── 09_EQUIPMENT.md
    ├── 10_ADVENTURING.md
    ├── 11_MONSTER_GUIDE.md
    ├── 12_MAGIC_ITEMS.md
    ├── 13_DM_GUIDE.md
    └── 14_CAMPAIGN_TEMPLATE.md
```

---

## Key Routes

| Route | Role | Description |
|-------|------|-------------|
| `/` | Any | Landing page |
| `/register` | Any | Create account (choose DM or Player role) |
| `/login` | Any | Log in |
| `/characters/new` | Player | Create a new character |
| `/characters/<id>` | Any | View character sheet |
| `/dm/dashboard` | DM | Campaign list + create campaign |
| `/dm/campaigns/<id>` | DM | Run campaign (narrate, manage combat, NPCs) |
| `/characters/template` | Any | Download `character_template.md` |
| `/characters/import` | Any | Import a character from an uploaded `.md` file |
| `/dm/campaigns/template` | DM | Download `campaign_template.md` |
| `/dm/campaigns/import` | DM | Import a campaign from an uploaded `.md` file |
| `/dm/impersonate/<uid>/campaign/<id>` | DM | Enter read-only player view for a campaign |
| `/dm/impersonate/exit` | DM | Exit impersonation and return to DM view |
| `/player/dashboard` | Player | See joined campaigns, manage characters |
| `/player/campaigns/<id>` | Player | Play in campaign (roll, attack, cast, skill check) |

---

## Notes

- Sessions are cookie-based (signed with `SECRET_KEY`)
- All game state (initiative order, combat log, narration) is stored as JSON in the `Campaign` table
- SQLite is appropriate for small groups (4–8 players); the `instance/` directory should be backed up to preserve campaign data
- The `Documentation/` folder contains D&D 5e reference material used to guide rules implementation — it is not served by the app
