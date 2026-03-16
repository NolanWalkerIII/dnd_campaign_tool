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

### Character Assignment (DM Tool)

- **DM Dashboard** — the "All Characters" list now shows each character's current owner (👤 username) or ⚠ Unassigned in red if unclaimed
- **Character sheet** — when a DM views any character, an **🔑 Ownership** card appears at the bottom: shows the current owner and a dropdown to reassign the character to any registered user (or set to Unassigned)
- Useful when a player creates a character the DM wants to claim, a character is abandoned, or the DM pre-builds characters to hand off

### DM Visibility & Player Impersonation

- **Who's Online** panel on the DM dashboard shows every player active in the last 5 minutes, with their character name and current HP
- **👁 View As** buttons appear next to each player in both the Who's Online panel and the Players list inside each campaign
- Clicking "View As" opens the campaign from that player's exact perspective — correct character list, initiative highlighting, and "your turn" banner
- A persistent banner across the top of every page shows "DM View: Viewing as [player] — actions are disabled" with an **Exit View** link
- All player action routes (roll, attack, skill check, cast spell) are blocked during impersonation — the DM cannot accidentally submit actions on a player's behalf

### Narration

- DM types scene narration; it appears in all player views under **Scene**
- Players see the latest narration prominently, with older entries collapsible

### Navigation

- **Left sidebar** on every page — role-gated: DM sees Campaigns, Characters, Rules, and DM Guide; Players see Campaigns, Characters, and Rules
- Collapses automatically on screens narrower than 900 px

### Combat

- **Initiative**: DM rolls for all participants (players + NPCs); order is sorted and displayed
- **Turn management**: Current turn highlighted with ⚡; players see a banner when it's their turn
- **Turn guardrails**: Attack and spell-cast actions are blocked server-side when combat is active and it is not the player's turn
- **Attack rolls**: Roll to-hit against optional target AC; damage dice resolved server-side; crits auto-double dice
- **Target dropdown**: During combat the attack form shows a dropdown of all combatants in the initiative order; an "Other…" option reveals a free-text field for custom targets
- **NPC combat interface**: DM can roll attacks on behalf of any NPC directly from the initiative order — pick target, set attack bonus, optional AC, and damage dice; result posts to the combat log
- **HP bar in header**: Active character HP is always visible at the top of the player campaign page — no scrolling required
- **Health tracking**: Damage applied to targets; death saves tracked when HP hits 0; conditions (Poisoned, Blinded, etc.) applied by DM
- **Combat log**: Timestamped log of all actions visible to everyone; DM can revert the last entry with one click
- **Party panel**: Players see all other party members (character name, class/level, HP bar) in the right column

### Skill Checks

Players can roll any skill check from their campaign page; result is posted to the combat log.

### Dice Roller

- **Dice dropdowns**: Two dropdowns (count 1–6 and die type d4/d6/d8/d10/d12/d20) replace the free-text field for quick common rolls
- Free-text expressions still accepted anywhere: `1d20`, `2d6+3`, `d8`, `4d6kh3`, etc.

### Spellcasting

- Cast a spell by name, slot level, and optional concentration flag
- Slot is consumed on cast; concentration replaces any existing concentration spell
- DM can end concentration on any character

### Rests

- **Short Rest**: Spend hit dice to recover HP (rolls hit die + CON modifier per die)
- **Long Rest**: Fully restores HP, resets all spell slots and hit dice

### AI Features (xAI Grok)

Requires `XAI_API_KEY` in `.env`. All keys are loaded from environment variables — never committed to source control.

- **✨ Clean Up narration** — refines the DM's raw narration text for grammar, atmosphere, and flow
- **🎲 Generate narration** — writes a new scene continuation based on the last 5 narration entries
- **AI Chapter Summary** — generates a vivid 2–4 sentence chapter recap using notes and recent combat log entries

### Story Progress & Chapter Tracker

- **Chapter timeline** — DM adds chapters with a title, description, and status (`Upcoming` / `Active` / `Completed`)
- **Status controls** — one-click buttons to set a chapter active, mark it complete, or reset it; only one chapter can be active at a time
- **DM Notes** — per-chapter notes panel (collapsible) for clues, reminders, and session prep
- **Story Forks** — each chapter can hold multiple named branches (e.g. "Follow the merchant" vs "Investigate the cave"); DM picks the one the party took, unchosen paths are preserved
- **AI Chapter Summary** — "✨ AI Summary" button generates a vivid 2–4 sentence recap using xAI Grok, reading the chapter notes and recent combat log for context; saved to the chapter and visible to players
- **Player view** — read-only progress timeline on the player campaign page shows chapter status, active fork, and any AI-generated summaries

---

## Project Structure

```
.
├── app.py                  # Flask application, routes, game logic
├── models.py               # SQLAlchemy models (User, Character, Campaign)
├── parsers.py              # Markdown parsers + template strings for import/export
├── api_routes.py           # REST API Blueprint (27 endpoints, Bearer token auth)
├── sms_routes.py           # Twilio SMS play-by-text Blueprint
├── game_data.py            # Races, classes, backgrounds, spell slot tables
├── services/
│   ├── ai.py               # xAI Grok API wrapper (narration, generation, chapter summary)
│   ├── ai_dm.py            # AI DM engine layer
│   ├── engine.py           # Pure-function game logic (extracted from routes)
│   ├── discord_bot.py      # Discord bot with slash commands + SMS bridge
│   └── sms.py              # Twilio SMS helpers
├── seed.py                 # Sample data for demo/playtesting
├── tests/
│   └── test_suite.py       # 38-test automated test suite
├── requirements.txt        # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── DOCKER.md               # Docker operations reference
├── PLAN.md                 # Full project plan and phase history
├── Feedback/               # Beta playtest feedback files
├── instance/
│   └── dnd.db              # SQLite database (created at runtime)
├── templates/
│   ├── base.html           # Shared layout: top nav + left sidebar
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── character_sheet.html
│   ├── character_create.html
│   ├── rules.html
│   ├── dm/
│   │   ├── dashboard.html
│   │   └── campaign.html
│   └── player/
│       ├── dashboard.html
│       └── campaign.html
└── Documentation/          # D&D 5e reference docs used during development
    └── *.md
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
| `/dm/characters/<id>/assign` | DM | Reassign character ownership to a different user |
| `/dm/impersonate/<uid>/campaign/<id>` | DM | Enter read-only player view for a campaign |
| `/dm/impersonate/exit` | DM | Exit impersonation and return to DM view |
| `/dm/campaigns/<id>/chapter/add` | DM | Add a chapter to the story tracker |
| `/dm/campaigns/<id>/chapter/<idx>/status` | DM | Set chapter status (upcoming/active/completed) |
| `/dm/campaigns/<id>/chapter/<idx>/notes` | DM | Save DM notes for a chapter |
| `/dm/campaigns/<id>/chapter/<idx>/delete` | DM | Delete a chapter |
| `/dm/campaigns/<id>/chapter/<idx>/fork/add` | DM | Add a story fork to a chapter |
| `/dm/campaigns/<id>/chapter/<idx>/fork/<i>/choose` | DM | Choose the active story fork |
| `/dm/campaigns/<id>/chapter/<idx>/summarize` | DM | AI-generate a chapter summary (JSON) |
| `/dm/campaigns/<id>/combat/log/revert` | DM | Remove the last combat log entry |
| `/dm/campaigns/<id>/npc/<idx>/attack` | DM | Roll an attack for an NPC combatant |
| `/player/dashboard` | Player | See joined campaigns, manage characters |
| `/player/campaigns/<id>` | Player | Play in campaign (roll, attack, cast, skill check) |

---

## Community Contributions

| Contributor | GitHub | Contribution |
|-------------|--------|-------------|
| BonzaiForest | [@JBEST2015](https://github.com/JBEST2015) | REST API layer (27 endpoints), Discord bot with slash commands, Twilio SMS play-by-text, AI DM engine, DM Settings page, Diagnostics page |

---

## Beta Playtesters

Thank you to the adventurers who joined the first beta session and provided invaluable feedback:

**Donut · Radster · Rolenquin · Tiodis**

Their playtest feedback directly shaped Phase 16 (combat UX improvements, party visibility, turn guardrails, and more).

---

## Notes

- Sessions are cookie-based (signed with `SECRET_KEY`)
- All game state (initiative order, combat log, narration) is stored as JSON in the `Campaign` table
- SQLite is appropriate for small groups (4–8 players); the `instance/` directory should be backed up to preserve campaign data
- The `Documentation/` folder contains D&D 5e reference material used to guide rules implementation — it is not served by the app
