# Campaign Codex

A web-based Dungeons & Dragons 5e campaign management tool. The Dungeon Master runs campaigns from a dedicated interface while players join and interact from their own browser windows — all in real time via a shared Flask server. Supports Discord slash commands, Twilio SMS play-by-text, and a REST API for AI agent gameplay.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask 3.1 |
| ORM | SQLAlchemy 2.0 + Flask-SQLAlchemy 3.1 |
| Database | SQLite (file: `instance/dnd.db`) |
| Frontend | HTML/CSS/JavaScript (Jinja2 templates, no heavy frameworks) |
| AI | xAI Grok (`grok-3-latest`) via `services/ai.py` |
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

# 3. Copy and fill in environment variables
cp .env.example .env

# 4. Start the server (port 5050 — macOS AirPlay blocks 5000)
PORT=5050 python app.py
# App is available at http://localhost:5050
```

### Option B — Docker (Local)

```bash
cp .env.example .env    # fill in API keys
docker compose up --build -d
# App is available at http://localhost:5001
```

The SQLite database is persisted in `./instance/` via a volume mount, so data survives container restarts.

### Option C — Docker (Production / VPS)

Production uses `docker-compose.prod.yml` which includes Traefik labels for HTTPS routing:

```bash
# Copy files to server, then:
docker-compose -f docker-compose.prod.yml up --build -d
```

> **Note**: Production servers use `docker-compose` (hyphenated, Compose v2). Local Mac/Linux installs use `docker compose` (space, Compose v3+).

---

## Environment Variables

Required in `.env` (never commit this file):

| Variable | Description |
|----------|-------------|
| `XAI_API_KEY` | xAI Grok API key — powers all AI features |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `DISCORD_CLIENT_ID` | Discord application ID |
| `CLAUDE_API_KEY` | Bearer token for REST API authentication |

Optional: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`

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
python -m pytest tests/test_suite.py -v
```

38 tests covering:
- Dice rolling (expressions, advantage/disadvantage, modifiers)
- Game logic (initiative, attack resolution, conditions, death saves)
- Authentication (register, login, logout, role enforcement)
- Character CRUD (creation, stat calculation, equipment, gold)
- DM workflows (campaign creation, player management, narration, NPC management)
- Player workflows (join campaign, skill checks, attack rolls, combat)
- Spell slots, casting, concentration, short/long rests, inventory

---

## User Roles

### Dungeon Master (DM)
- Register with role **DM** at `/register`
- Full access to all character sheets (read + edit)
- Can adjust any character's HP, grant/revoke Inspiration, and manage combat
- Sees which players are currently online (active within 5 minutes)
- Can impersonate any player to see exactly what they see (read-only — no actions)

### Player
- Register with role **Player** at `/register`
- Creates and manages their own characters
- Joins campaigns via a campaign code provided by the DM
- Actions scoped to their own characters only

---

## Feature Overview

### Characters

- **AI Character Generator** — "New Character" offers two paths: generate with AI or fill in manually. The AI wizard takes race, class, background, alignment, and optional story prompts (origin, drive, flaw, and any other details) and generates a full character via xAI Grok. A preview/approval page shows the proposed name, ability scores, backstory, traits, and appearance before anything is saved. Regenerate as many times as needed.
- **Manual creation wizard** — select race (with ASI bonuses), class, background, alignment, ability scores (standard array), and skill proficiencies
- **Character sheet** — full stat block: ability scores + modifiers, proficiency bonus, AC, speed, saving throws, skills; Temp HP field; Passive Perception/Investigation/Insight; Senses and Languages from race; Background Feature
- **Tab interface** — bottom half organized into tabs: Saves & Skills | Inventory | Spells | Features | Background | Rests; tab state persisted per-character via localStorage
- **Background Tab** — editable fields for Custom Background, Personality Traits, Ideals, Bonds, Flaws, Physical Characteristics (height, weight, age, eyes, hair, skin, gender), and Appearance; all stored in `character.spells['background_details']`
- **Inspiration** — gold star pill on character sheet; "Spend" button when active; DM grants/revokes from campaign page
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

#### Characters (v2 format)

- **⬇ Download Template** delivers a pre-filled `character_template.md`
- **Import Character** — upload a filled-in `.md` file to create a character instantly, skipping the form
- Imported ability scores are accepted as-is (not restricted to the standard array), making it easy to bring in existing characters
- Class and background starting equipment + gold are added on top of anything in the file
- All Background Tab fields import automatically and populate `background_details` on the character sheet

Character template sections: `## Basic Info`, `## Ability Scores`, `## Skill Proficiencies`, `## Equipment`, `## Gold`, `## Physical Characteristics`, `## Backstory`, `## Personality Traits`, `## Ideals`, `## Bonds`, `## Flaws`, `## Appearance`

#### Campaigns (v2 format)

- **⬇ Download Template** delivers `campaign_template.md`
- **Import Campaign** — upload a filled-in `.md` file to create a campaign with opening narration, NPC presets, and chapter tracker pre-loaded
- NPC presets appear in a **📋 Imported NPC Presets** card with one-click **⚔ Add to Combat** buttons
- NPCs support `Scene:` and `Dialogue:` fields (multiline) that import as rich notes
- Chapters import fully: title, description, status, DM notes, and named story branches

Campaign template sections: `## Campaign Info`, `## Opening Narration`, `## Chapters` (with `### Chapter: Title` blocks), `## NPCs` (each NPC as a `### Name` block with `HP:`, `AC:`, `Initiative Bonus:`, `Scene:`, `Dialogue:`, `Notes:`)

### DM Inspiration

- **Grant / Revoke** — toggle button per character in the Players section of the DM campaign page
- **Character sheet** — gold ★ pill when inspired; muted ☆ when not; "Spend" button for players to consume it
- **Spend** — sets inspiration to false; callable by the player or DM

### Story Progress & Chapter Tracker

- **Chapter timeline** — DM adds chapters with a title, description, and status (`Upcoming` / `Active` / `Completed`)
- **Status controls** — one-click buttons to set a chapter active, mark it complete, or reset it; only one chapter can be active at a time
- **DM Notes** — per-chapter notes panel (collapsible) for clues, reminders, and session prep
- **Story Forks** — each chapter can hold multiple named branches; DM picks the one the party took; unchosen paths preserved
- **AI Chapter Summary** — generates a vivid 2–4 sentence recap using xAI Grok, reading chapter notes and recent combat log for context; saved to the chapter and visible to players
- **Player view** — read-only progress timeline shows chapter status, active fork, and AI-generated summaries

### Combat

- **Initiative** — DM rolls for all participants (players + NPCs); order sorted and displayed
- **Turn management** — current turn highlighted with ⚡; players see a banner when it's their turn
- **Turn guardrails** — attack and spell-cast actions are blocked server-side when combat is active and it is not the player's turn
- **Attack rolls** — roll to-hit against optional target AC; damage dice resolved server-side; crits auto-double dice
- **Target dropdown** — during combat the attack form shows a dropdown of all combatants; "Other…" option reveals a free-text field
- **NPC combat interface** — DM can roll attacks on behalf of any NPC directly from the initiative order
- **HP bar in header** — active character HP always visible at the top of the player campaign page
- **Health tracking** — damage applied to targets; death saves tracked when HP hits 0; conditions applied by DM
- **Combat log** — timestamped log of all actions; DM can revert the last entry with one click
- **Party panel** — players see all party members (name, class/level, HP bar) in the right column

### Skill Checks & Dice Roller

- Players roll any skill check from their campaign page; result posts to the combat log
- **Dice dropdowns** — count (1–6) and die type (d4/d6/d8/d10/d12/d20) dropdowns for quick common rolls
- Free-text expressions still accepted: `1d20`, `2d6+3`, `4d6kh3`, etc.

### Spellcasting

- Cast a spell by name, slot level, and optional concentration flag
- Slot consumed on cast; concentration replaces any existing concentration spell
- DM can end concentration on any character

### Rests

- **Short Rest** — spend hit dice to recover HP (rolls hit die + CON modifier per die)
- **Long Rest** — fully restores HP, resets all spell slots and hit dice

### AI Features (xAI Grok)

Requires `XAI_API_KEY` in `.env`.

**Narration (DM)**
- **✨ Clean Up narration** — refines the DM's raw text for grammar, atmosphere, and flow
- **🎲 Generate narration** — writes a new scene continuation from the last 5 narration entries

**Character Background Tab**
- **✨ Clean Up** — polishes existing custom background text
- **🎲 Generate backstory** — creates a 2–4 paragraph origin story from character info
- **🎲 Generate traits** — generates Personality Traits, Ideals, Bonds, or Flaws individually (requires custom background first)
- **🎲 Generate appearance** — describes physical appearance (requires background + at least one physical characteristic)

**Character Generator Wizard**
- Wizard form → xAI Grok generates: name, backstory, personality traits, ideals, bonds, flaws, appearance, ability score priority order, and suggested skills
- Preview page shows full character before anything is saved; Regenerate for a fresh take

**AI Player Mode (DM Tool)**

Requires `XAI_API_KEY`. Enables the DM to assign AI-controlled personas to characters, useful for solo play, practice sessions, and filling empty player slots.

- **Enable AI Player** — toggle per character from the campaign page; choose persona level: `Novice`, `Intermediate`, or `Experienced`
- **🎲 Take Action** — generate an in-character action for any AI-controlled character; shows a preview with Post / Edit & Post / Discard options
- **🤖 All AI Players — Take Action** — batch trigger that sequentially generates actions for every AI-controlled character in one click
- **🤖 AI Turn** — appears on the active combatant's row in the initiative order when that character is AI-controlled; generates a structured combat decision (action type, target, weapon/spell, bonus action, reasoning) for DM review; Execute or Skip
- **🎭 Hot Seat** — DM temporarily overrides any AI character to type a single action themselves; posts as that character
- **DM-Managed Characters** — DM can add characters (not linked to any player login) directly to the campaign roster; they receive the same HP, inspiration, and AI controls as regular player characters

**Practice Mode**

- **🎓 Practice Mode toggle** — when all active characters are AI-controlled, the DM can enable Practice Mode; a gold banner marks the session
- **⏭ Advance Party** — generates actions for every AI character in sequence; each result shown for DM review before posting
- **📊 Session Summary** — dedicated page showing all AI characters, narration log, combat log, and an AI-generated coaching debrief (what each persona did well, what a real player at that level might do differently, and 2–3 actionable tips for the DM)

### Admin Console

Accessible to accounts with the `is_admin` flag. Promote a user via the Docker CLI (see below). The **🛡 Admin Console** link appears in the sidebar for admins after login.

- **Dashboard** — stats cards (total users, campaigns, characters), recent signups, recent admin action history
- **User list** — searchable/filterable table of all accounts with role, last-seen, and ban status
- **User detail** — full profile: linked characters, DM campaigns, action history; all management actions available in one place
- **Reset password** — generates a secure 12-character temporary password displayed to the admin; the user is forced to change it on next login
- **Ban / Unban** — suspended accounts see "Account suspended" on login and cannot log in
- **Set role** — promote Player → DM or demote DM → Player without touching the database
- **Grant / Revoke admin** — delegate admin access to other users
- **Delete user** — soft-deletes the account; their characters are orphaned (kept for campaign history) rather than cascade-deleted
- **Audit log** — every admin action is recorded (who, what, when, on which account) and shown on the dashboard and user detail pages

**Promoting the first admin:**
```bash
docker exec dndidea-dnd-1 python -c "
from app import app
from models import db, User
with app.app_context():
    u = User.query.filter_by(username='YOUR_USERNAME').first()
    u.is_admin = True
    db.session.commit()
"
```

### Character Assignment (DM Tool)

- DM dashboard shows each character's current owner or ⚠ Unassigned
- DM can reassign any character to any registered user from the character sheet

### DM Visibility & Player Impersonation

- **Who's Online** panel shows every player active in the last 5 minutes
- **👁 View As** buttons open the campaign from that player's exact perspective
- A persistent banner shows "DM View: Viewing as [player]" with an **Exit View** link
- All player action routes are blocked during impersonation

### Discord Integration

- Slash commands for DM: `/setup`, `/start`, `/reset`, `/scene`, `/combat`, `/npc`, `/damage`, `/heal`, `/whisper`, `/recap`, `/agent`
- Slash commands for players: `/join`, `/verify`, `/action`, `/roll`, `/attack`, `/check`, `/stats`

### SMS Play Mode (Twilio)

- Players can participate via text message using the Twilio webhook at `/sms`
- AI DM interprets player actions and responds with narrated outcomes

### REST API

- 27 endpoints under `/api/` with Bearer token authentication
- Supports AI agent gameplay — get game context, submit actions, read logs

---

## Project Structure

```
.
├── app.py                  # Flask application, routes, game logic
├── models.py               # SQLAlchemy models (User, Character, Campaign, AdminAuditLog)
├── parsers.py              # Markdown parsers + v2 template strings for import/export
├── api_routes.py           # REST API Blueprint (27 endpoints, Bearer token auth)
├── sms_routes.py           # Twilio SMS play-by-text Blueprint
├── game_data.py            # Races, classes, backgrounds, spell slot tables
├── services/
│   ├── ai.py               # xAI Grok wrapper (narration, background, character generation)
│   ├── ai_dm.py            # AI DM engine layer
│   ├── ai_player.py        # AI Player mode (out-of-combat actions, combat decisions, practice debrief)
│   ├── engine.py           # Pure-function game logic (rolls, attacks, skill checks)
│   ├── discord_bot.py      # Discord bot with slash commands
│   └── sms.py              # Twilio SMS helpers
├── seed.py                 # Sample data for demo/playtesting
├── tests/
│   └── test_suite.py       # 38-test automated test suite
├── requirements.txt        # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml # Production docker-compose
├── DOCKER.md               # Docker operations reference
├── PLAN.md                 # Full project plan and phase history (Phases 1–29, all complete)
├── instance/
│   └── dnd.db              # SQLite database (created at runtime)
├── static/
│   ├── favicon/            # Favicons (ico, 16, 32, apple-touch)
│   └── img/
│       ├── logo/           # campaign-codex-dark.png, campaign-codex-light.png
│       ├── icon/           # codex-icon.png
│       └── monogram/       # cc-monogram.png
├── templates/
│   ├── base.html           # Shared layout: top nav + left sidebar
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── change_password.html     # Forced password change after admin reset
│   ├── character_sheet.html
│   ├── character_create.html    # Two-path: AI generator or manual form
│   ├── character_generate.html  # AI generator wizard form
│   ├── character_preview.html   # AI character preview + approve/regenerate
│   ├── rules.html
│   ├── admin/
│   │   ├── dashboard.html       # Stats overview + recent users + audit log
│   │   ├── users.html           # Searchable user list
│   │   └── user_detail.html     # User profile, actions, characters, campaigns
│   ├── dm/
│   │   ├── dashboard.html
│   │   ├── campaign.html
│   │   └── practice_summary.html  # Practice Mode session summary + AI debrief
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
| `/characters/new` | Player | New character — AI generator or manual |
| `/characters/generate` | Player | AI character generator wizard |
| `/characters/generate/preview` | Player | Preview AI-generated character |
| `/characters/generate/confirm` | Player | Approve and create AI character |
| `/characters/generate/regenerate` | Player | Regenerate with same inputs |
| `/characters/<id>` | Any | View character sheet |
| `/characters/<id>/background_details` | Owner/DM | Save background tab fields |
| `/characters/<id>/temp_hp` | Owner/DM | Set temporary HP |
| `/characters/<id>/inspiration/spend` | Owner/DM | Spend inspiration |
| `/characters/<id>/ai/background/generate` | Owner/DM | AI-generate backstory |
| `/characters/<id>/ai/background/cleanup` | Owner/DM | AI-polish backstory |
| `/characters/<id>/ai/trait` | Owner/DM | AI-generate a trait field |
| `/characters/<id>/ai/appearance` | Owner/DM | AI-generate appearance |
| `/characters/template` | Any | Download character template (v2) |
| `/characters/import` | Any | Import character from `.md` file |
| `/dm/dashboard` | DM | Campaign list + create campaign |
| `/dm/campaigns/<id>` | DM | Run campaign (narrate, combat, NPCs) |
| `/dm/campaigns/template` | DM | Download campaign template (v2) |
| `/dm/campaigns/import` | DM | Import campaign from `.md` file |
| `/dm/characters/<id>/assign` | DM | Reassign character ownership |
| `/dm/characters/<id>/inspiration` | DM | Grant/revoke inspiration |
| `/dm/impersonate/<uid>/campaign/<id>` | DM | Enter read-only player view |
| `/dm/impersonate/exit` | DM | Exit impersonation |
| `/dm/campaigns/<id>/chapter/add` | DM | Add a chapter |
| `/dm/campaigns/<id>/chapter/<idx>/status` | DM | Set chapter status |
| `/dm/campaigns/<id>/chapter/<idx>/notes` | DM | Save DM notes |
| `/dm/campaigns/<id>/chapter/<idx>/fork/add` | DM | Add story fork |
| `/dm/campaigns/<id>/chapter/<idx>/fork/<i>/choose` | DM | Choose active fork |
| `/dm/campaigns/<id>/chapter/<idx>/summarize` | DM | AI chapter summary |
| `/dm/campaigns/<id>/combat/log/revert` | DM | Revert last combat log entry |
| `/dm/campaigns/<id>/npc/<idx>/attack` | DM | Roll attack for NPC |
| `/dm/campaigns/<id>/add-managed-char` | DM | Add DM-managed character to campaign |
| `/dm/campaigns/<id>/remove-managed-char` | DM | Remove DM-managed character |
| `/dm/campaigns/<id>/practice-mode/toggle` | DM | Enable/disable Practice Mode |
| `/dm/campaigns/<id>/practice-summary` | DM | Practice session summary page |
| `/dm/campaigns/<id>/practice-summary/generate` | DM | Generate AI coaching debrief |
| `/dm/characters/<id>/ai-toggle` | DM | Enable/disable AI Player for a character |
| `/dm/characters/<id>/ai-level` | DM | Set AI persona level (novice/intermediate/experienced) |
| `/dm/characters/<id>/ai-action` | DM | Generate out-of-combat AI action |
| `/dm/characters/<id>/ai-action/post` | DM | Post AI action to narration log |
| `/dm/characters/<id>/ai-combat-turn` | DM | Generate AI combat decision |
| `/dm/characters/<id>/ai-combat-execute` | DM | Execute approved AI combat action |
| `/player/dashboard` | Player | Dashboard — campaigns + characters |
| `/player/campaigns/<id>` | Player | Play in campaign |
| `/change-password` | Any | Change own password (forced after admin reset) |
| `/admin` | Admin | Admin dashboard — stats + recent activity |
| `/admin/users` | Admin | User list with search |
| `/admin/users/<id>` | Admin | User detail + management actions |
| `/admin/users/<id>/reset-password` | Admin | Generate temporary password |
| `/admin/users/<id>/toggle-ban` | Admin | Ban or unban account |
| `/admin/users/<id>/set-role` | Admin | Change user role |
| `/admin/users/<id>/toggle-admin` | Admin | Grant or revoke admin access |
| `/admin/users/<id>/delete` | Admin | Delete user (orphans characters) |

---

## Community Contributions

| Contributor | GitHub | Contribution |
|-------------|--------|-------------|
| BonzaiForest | [@JBEST2015](https://github.com/JBEST2015) | REST API layer (27 endpoints), Discord bot with slash commands, Twilio SMS play-by-text, AI DM engine, DM Settings page, Diagnostics page |

---

## Beta Playtesters

Thank you to the adventurers who joined the first beta session and provided invaluable feedback:

**Donut · Radster · Rolenquin · Tiodis**

Their feedback directly shaped Phase 16 (combat UX improvements, party visibility, turn guardrails, and more).

---

## Notes

- Sessions are cookie-based (signed with `SECRET_KEY`)
- All game state (initiative order, combat log, narration, chapters) is stored as JSON in the `Campaign` table
- Character background details, inspiration, temp HP, hit dice, and spell slots are stored in the `Character.spells` JSON column; use `flag_modified(obj, 'spells')` after any mutation
- SQLite is appropriate for small groups (4–8 players); back up `instance/` to preserve campaign data
- The `Documentation/` folder contains D&D 5e reference material used to guide rules implementation — it is not served by the app
