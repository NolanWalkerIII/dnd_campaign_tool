# Plan for D&D Campaign Management Application

Based on the analysis of the D&D documentation, I'll outline a comprehensive plan to build a text-based D&D application where the Dungeon Master (DM) manages campaigns and players interact through separate interfaces. The focus will be on core functionality: character management, dice rolling, and game state tracking, starting with text-based interfaces before adding visual elements like maps.

## Project Overview
- **Goal**: A web-based application (initially text-focused) allowing DMs to run campaigns and players to participate via individual browser interfaces.
- **Tech Stack**: 
  - Backend: Python with Flask (lightweight web framework for handling game logic and state).
  - Frontend: HTML/CSS/JavaScript (simple forms and text displays for input/output).
  - Database: SQLite (for storing characters, campaigns, and game state).
  - Deployment: Local development first, with potential for cloud hosting later.
- **Architecture**: Client-server model where the Flask server manages shared game state, and each user (DM + players) has a dedicated web interface.
- **Key Constraints**: Start with text-based interactions; no maps or graphics initially. Focus on core mechanics from the documentation (dice rolling, combat, character sheets).

## Core Requirements Breakdown
From the documentation analysis, the essential features to implement:
- **Character Management**: Creation (race, class, ability scores), stat tracking (HP, AC, proficiency), equipment.
- **Dice System**: Rolling d4-d20 with modifiers, advantage/disadvantage, critical hits.
- **Combat**: Initiative, turn order, attack rolls, damage, conditions (e.g., poisoned, unconscious).
- **Game Flow**: Exploration (skill checks), encounters, rests (short/long).
- **DM Tools**: Campaign setup, NPC management, narration, action resolution.
- **Player Tools**: Character viewing, action input (rolls, attacks), status updates.

## Phased Implementation Plan

### Phase 1: Project Setup and Core Data Models (1-2 days)
- **Objectives**: Establish the foundation with basic classes and a simple web server.
- **Tasks**:
  1. Set up Python environment (venv) and install Flask, SQLAlchemy (for database ORM).
  2. Define core data models:
     - `Character`: Ability scores, HP, AC, proficiency bonus, skills, equipment, spells.
     - `Campaign`: DM ID, list of players/NPCs, current game state (initiative order, active conditions).
     - `DiceRoller`: Utility class for rolling dice (support modifiers, advantage/disadvantage).
  3. Implement basic Flask routes for serving static pages.
  4. Create a simple "Hello World" web page to verify setup.
- **Deliverables**: Functional Flask app with models; basic dice rolling tested via console.
- **Validation**: Run unit tests for dice rolls and model creation.
- **Status**: Completed

### Phase 2: Character Creation and Management (2-3 days)
- **Objectives**: Allow users to create and view characters based on D&D rules.
- **Tasks**:
  1. Build character creation wizard (web form):
     - Race selection (with ASI bonuses, e.g., +2 STR for Half-Orc).
     - Class selection (with proficiencies, e.g., Fighter gets armor/weapon profs).
     - Ability score assignment (standard array or point buy).
     - Background and equipment selection.
  2. Implement character sheet display (read-only view for stats, HP, skills).
  3. Add database persistence for characters.
  4. Basic validation (e.g., ensure ability scores sum correctly).
- **Deliverables**: Web forms for character creation; saved characters viewable in database.
- **Validation**: Create test characters for each class; verify stat calculations (e.g., modifiers, AC).
- **Status**: Complete ✓ (character creation wizard, sheet view, character list all implemented)

### Phase 3: Basic User Interfaces and Session Management (2-3 days)
- **Objectives**: Separate DM and player interfaces; handle user sessions.
- **Tasks**:
  1. Implement user authentication (simple username/password for DM/players).
  2. DM Interface:
     - Dashboard: List active players, start/end campaigns, narrate scenes (text input).
     - View all character sheets; manually adjust stats (e.g., apply damage).
  3. Player Interface:
     - Dashboard: View own character; input actions (e.g., "Roll initiative").
     - Real-time updates for game state (polling or basic WebSockets if needed).
  4. Campaign joining: Players enter a campaign code to join DM's session.
- **Deliverables**: Functional web pages for DM and players; session-based access control.
- **Validation**: Test multi-user access (run multiple browser tabs); ensure DM can see all players.
- **Status**: Complete ✓ (auth, DM dashboard/campaign, player dashboard/campaign, HP adjustment all implemented)

### Phase 4: Core Game Mechanics - Dice and Combat (3-4 days)
- **Objectives**: Implement rolling and basic combat loop.
- **Tasks**:
  1. Enhance DiceRoller: Support multiple dice (e.g., 2d6 + 3), advantage/disadvantage.
  2. Combat System:
     - Initiative: Roll for all participants; sort turn order.
     - Turn Management: Track current turn; allow actions (attack, move, bonus action).
     - Attack Resolution: Roll to hit, calculate damage, apply to targets.
     - Health Tracking: Update HP, handle death saves, conditions.
  3. Action Inputs: Players/DM submit actions via forms; server resolves and broadcasts updates.
  4. Basic Exploration: Skill checks (e.g., Perception) outside combat.
- **Deliverables**: Full combat loop playable; dice rolls logged and displayed.
- **Validation**: Simulate a short combat encounter; verify initiative order and damage calculations.
- **Status**: Complete ✓ (initiative, turn management, attack resolution, skill checks, conditions, death saves all implemented)

### Phase 5: Advanced Features and Polish (2-3 days)
- **Objectives**: Add spellcasting, equipment, and refinements.
- **Tasks**:
  1. Spellcasting: Track spell slots, casting (with components), concentration.
  2. Equipment Management: Inventory, weapon/armor stats, gold tracking.
  3. Rest System: Short/long rests to reset resources.
  4. Error Handling: Validate inputs (e.g., prevent invalid rolls); add undo for mistakes.
  5. UI Polish: Improve text displays; add basic styling for readability.
- **Deliverables**: Complete core gameplay loop; documented API for future extensions.
- **Validation**: End-to-end test of a full session (character creation → combat → rest).
- **Status**: Complete ✓ (spellcasting slots/cast/concentration, hit dice, short/long rests, inventory add/remove, gold tracking, UI sections on character sheet and campaign pages)

### Phase 6: Testing, Deployment, and Future Roadmap (1-2 days)
- **Objectives**: Ensure stability and plan expansions.
- **Tasks**:
  1. Write unit/integration tests for key functions (dice, combat).
  2. User testing: Run playtests with sample scenarios.
  3. Deployment: Package as a runnable app (e.g., via Docker for local/cloud).
  4. Future Phases: Add maps (e.g., ASCII art or simple grid), audio narration, mobile support.
- **Deliverables**: Deployable app; test suite; roadmap document.
- **Validation**: Full regression testing; gather feedback for improvements.
- **Status**: Complete ✓ (38-test suite covering dice, game logic, auth, character CRUD, DM/player workflows, Phase 5 features; Dockerfile + docker-compose for deployment; seed.py for playtest data)

---

## Post-Playtest Feature Roadmap
*Based on feedback collected in `Testing_1.md` after Phase 6 playtesting.*

### Phase 7: DM Visibility & Player Impersonation
- **Objectives**: Give the DM better situational awareness and a way to troubleshoot player views.
- **Tasks**:
  1. **Who's Online panel** on the DM dashboard: track last-seen timestamp per user on each request; display a live list of players currently in the session (last active within 5 minutes), with their character name and HP.
  2. **Impersonate Player**: DM-only route (`/dm/impersonate/<user_id>`) that sets a session flag (`impersonating_user_id`) and redirects to the player's campaign view. A persistent banner shows "Viewing as [Player]" with an **Exit** link that clears the flag and returns to the DM dashboard. Impersonation is read-only — no actions can be submitted while impersonating.
  3. Add `last_seen` timestamp column to the `User` model; update it via a `before_request` hook.
- **Deliverables**: Online player list on DM dashboard; impersonate/exit flow; read-only guard on player action routes.
- **Validation**: DM can see alice and bob as online after they load the campaign page; DM can view alice's exact campaign page with the "Viewing as" banner visible.
- **Status**: Complete ✓ (`last_seen` column on User; `before_request` hook; `/dm/impersonate/<uid>/campaign/<id>` and `/dm/impersonate/exit` routes; `player_required` allows DM impersonators; `_effective_uid()` / `_check_not_impersonating()` helpers; all four player action POST routes blocked during impersonation; Who's Online panel on DM dashboard; 👁 View As buttons on DM campaign page; impersonation banner in base.html)

### Phase 8: Markdown Import / Export for Characters & Campaigns
- **Objectives**: Allow reusable, portable character sheets and campaign setups via `.md` files.
- **Tasks**:
  1. **Character Markdown Template**:
     - Add a **Download Template** button on the character creation page that delivers a pre-filled `.md` file with all required fields and instructions.
     - Add an **Import from Markdown** button on the character creation page; accepts a `.md` file upload, parses key/value fields (name, race, class, ability scores, background, skills, equipment, gold), and pre-fills the creation form or directly creates the character.
  2. **Campaign Markdown Import**:
     - Define a campaign bundle format: a primary `campaign.md` (name, description, narration scenes, dialog zones) plus optional companion files (`npcs.md`, `encounters.md`). Provide a **Download Template** zip from the DM dashboard.
     - Add **Import Campaign** on the DM dashboard: upload a `.md` (or zip of `.md` files); parse and create a new Campaign with pre-loaded NPCs, encounters, and opening narration.
  3. Create a `parsers.py` module with `parse_character_md(text)` and `parse_campaign_md(text)` helpers.
  4. Keep templates human-readable with `## Section` headers and `Key: Value` lines so DMs can edit them in any text editor.
- **Deliverables**: Download template buttons for characters and campaigns; upload/import flows; `parsers.py`; sample `.md` templates in `Documentation/`.
- **Validation**: Download character template → edit in a text editor → import → verify character is created with correct stats. Download campaign template → fill in NPCs and opening narration → import → verify campaign loads with that content.
- **Status**: Complete ✓ (`parsers.py` with `parse_character_md` / `parse_campaign_md` / template strings; `GET /characters/template` download; `POST /characters/import` create character; `GET /dm/campaigns/template` download; `POST /dm/campaigns/import` create campaign with narration + NPC presets; Download Template + import form on character creation page; Import Campaign collapsible on DM dashboard; Imported NPC Presets card with "Add to Combat" quick-fill buttons on DM campaign page)

### Phase 9: AI-Powered Narration (xAI Grok)
- **Objectives**: Let the DM polish or generate narration text on the fly using xAI Grok.
- **⚠ Security Note**: The xAI API key MUST be stored in a `.env` file and excluded from version control via `.gitignore`. It must never be hard-coded in source files.
- **Tasks**:
  1. Add `python-dotenv` and `requests` (or the xAI SDK) to `requirements.txt`.
  2. Create `.env` (gitignored) with `XAI_API_KEY=...`; create `.env.example` with a placeholder that IS committed.
  3. Add `XAI_API_KEY` as an environment variable in `docker-compose.yml` (sourced from `.env` via `env_file:`).
  4. **Clean Up Narration** button on the DM campaign page: takes the current text in the narration input box, sends it to Grok with a prompt like *"Clean up and refine this D&D narration, keeping the tone and content but improving clarity and atmosphere"*, and replaces the textarea content with the result (JS fetch to a `/dm/campaigns/<id>/ai/cleanup` route). The DM can review before posting.
  5. **Generate Narration** button: reads the last N entries from the narration log, sends them to Grok as context with a prompt like *"Continue this D&D campaign narration with a compelling next scene"*, and populates the textarea for the DM to review and post.
  6. Add a `services/ai.py` module that wraps the xAI API call so the key is only referenced in one place.
  7. Both AI routes return JSON `{ "text": "..." }` and fail gracefully (return an error message) if the API key is missing or the request fails.
- **Deliverables**: `.env.example`; `services/ai.py`; two DM-only AI routes; Clean Up and Generate buttons on the DM campaign page.
- **Validation**: With a valid API key, both buttons populate the narration textarea with Grok-generated text; without a key, a friendly error message is shown instead of a crash.
- **Status**: Complete ✓ (`.env.example` + `.gitignore`; `python-dotenv` + `requests` in requirements; `services/ai.py` with `cleanup_narration` / `generate_narration` wrapping xAI Grok API with graceful error handling; `POST /dm/campaigns/<id>/ai/cleanup` and `/ai/generate` JSON routes; `docker-compose.yml` loads `.env` via `env_file`; ✨ Clean Up and 🎲 Generate buttons on DM campaign narration form using `fetch` — populate textarea for DM review before posting)

### Phase 10: Campaign Save & Load
- **Objectives**: Let the DM export and restore full campaign state so nothing is ever lost.
- **Tasks**:
  1. **Save Campaign** (`/dm/campaigns/<id>/save`): Serialize the full campaign state (name, narration log, combat state, NPC list, all joined characters' current stats) to a timestamped JSON file downloaded to the DM's browser (`campaign_<name>_<timestamp>.json`).
  2. **Load Campaign** (`/dm/campaigns/<id>/load`): Accept a previously-saved JSON file upload; validate its schema; restore campaign state (narration log, NPCs, combat state). Character HP/slots are updated in the database. Existing campaign record is overwritten — a confirmation prompt is shown first.
  3. Add **Save** and **Load** buttons to the DM campaign page in a "Campaign Management" card.
  4. The save format is versioned (`"schema_version": 1`) so future changes can handle migration gracefully.
- **Deliverables**: Save (download JSON) and Load (upload JSON) routes; buttons on DM campaign page; schema versioning.
- **Validation**: Run a combat encounter → save → restart the server → load the save → verify initiative order, combat log, and HP values are restored exactly.
- **Status**: Complete ✓ (`GET /dm/campaigns/<id>/save` downloads a versioned JSON snapshot of the campaign state + all player character HP/slots/equipment; `POST /dm/campaigns/<id>/load` validates schema version and campaign ID, restores `current_state`, player list, and individual character records; 💾 Save link and 📂 Load toggle in page header; load panel shows warning + confirm dialog before overwriting; save filename is `<campaign_name>_<timestamp>.json`)

---

## Post-Phase 10 Feature Roadmap
*Based on feedback collected in `Testing_2.md` after Phase 10 playtesting.*

### Phase 11: In-App Rules Reference & DM Guide Tabs
- **Objectives**: Surface the existing Documentation folder as a navigable in-app reference so players and the DM can look up rules without leaving the browser.
- **Tasks**:
  1. Add a `/rules` route that renders a reference hub page with tabs (or a sidebar) linking to the key sections: Core Mechanics, Combat, Spellcasting, Conditions, Equipment, Classes, Races, Adventuring.
  2. Add a `/dm/guide` route (DM-only) that renders the DM Guide and NPC/Encounter template reference.
  3. Parse the existing `Documentation/*.md` files server-side with Python's `markdown` library and render them as styled HTML within the app's base template.
  4. Add **Rules** and **DM Guide** links to the nav bar — Rules visible to all logged-in users, DM Guide only to DMs.
  5. Add a **Quick Reference** card on the player campaign page listing the most common actions (Attack, Dash, Dodge, Help, Hide, Ready, Search, Disengage) with one-line descriptions.
- **Deliverables**: `/rules` hub page; `/dm/guide` page; nav bar links; Quick Reference card on player campaign page; `markdown` added to `requirements.txt`.
- **Validation**: All documentation sections render correctly; DM Guide is inaccessible to players; Quick Reference card is visible during a campaign.
- **Status**: Complete ✓ (markdown library added; /rules and /dm/guide routes with sidebar nav; rules.html template; nav bar links; Quick Reference card on player campaign page)

### Phase 12: Campaign Onboarding & Join Walkthrough
- **Objectives**: Make it obvious to new DMs and players how to get a session started — eliminate the "where do I go?" confusion.
- **Tasks**:
  1. **DM Campaign Onboarding Card**: After a campaign is created (or on first visit with no players joined), show a step-by-step "Getting Started" card on the DM campaign page:
     - Step 1: Share the join code with your players (display it large with a copy-to-clipboard button).
     - Step 2: Players go to `http://<your-host>:5001`, register, and enter the code on their dashboard.
     - Step 3: Once players have joined, click "Start Combat" or write your first narration.
     - Dismiss button persists the dismissal in `current_state` so it doesn't reappear.
  2. **Player Join Walkthrough**: On the player dashboard, if the player has no campaigns, show a prominent "Join a Campaign" card with clear instructions and the join code input front and center.
  3. Add a shareable **Campaign Info** panel on the DM campaign page: hostname/port, join code (large), and QR code (generated client-side via a small JS library) that encodes the join URL.
- **Deliverables**: DM onboarding card with dismissal; player join walkthrough card; Campaign Info panel with copy button and QR code.
- **Validation**: A brand-new DM can get players into a session using only the in-app guidance — no external docs needed.
- **Status**: Complete ✓ (DM onboarding card with dismiss; Campaign Info panel with join URL, large code, QR code via lazy-loaded qrcodejs on `<details>` toggle; player join walkthrough card when no campaigns joined)

---

## Community Contributions — BonzaiForest / JBEST2015
*Major feature expansion contributed by [BonzaiForest (JBEST2015)](https://github.com/JBEST2015), merged into `main` March 2026.*

### REST API Layer (`api_routes.py` — ~1,300 lines)
A full authenticated REST API (`/api/*`) secured with a Bearer token (`CLAUDE_API_KEY`). Enables external clients (Claude, Discord bot, SMS) to drive the game engine programmatically.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/campaigns` | GET | List all campaigns |
| `/api/campaigns/<id>` | GET | Full campaign state + characters |
| `/api/characters/<id>` | GET | Character sheet JSON |
| `/api/action` | POST | Free-text action — AI interprets and resolves |
| `/api/roll` | POST | Dice roll for a character |
| `/api/skill-check` | POST | Skill check with proficiency |
| `/api/attack` | POST | Attack roll + damage vs target |
| `/api/saving-throw` | POST | Saving throw |
| `/api/scene` | POST | Post new narration to the campaign |
| `/api/npc/say` | POST | NPC dialogue via AI |
| `/api/combat/start` | POST | Roll initiative and start combat |
| `/api/combat/next` | POST | Advance turn |
| `/api/combat/end` | POST | End combat |
| `/api/damage` | POST | Apply damage to combatant |
| `/api/heal` | POST | Heal a combatant |
| `/api/condition` | POST | Apply/remove condition |
| `/api/loot` | POST | Award loot to a player |
| `/api/npc/add` | POST | Add NPC to initiative |
| `/api/npc/remove` | POST | Remove NPC |
| `/api/discord/send` | POST | Send message to Discord channel |
| `/api/discord/embed` | POST | Send rich embed to Discord |
| `/api/discord/status` | GET | Discord bot connection status |
| `/api/diagnostics` | GET | Full system health check |
| `/api/diagnostics/test/<name>` | POST | Run individual diagnostic test |
| `/api/log/<id>` | GET | Paginated narration log |
| `/api/play` | POST | AI DM turn — interprets free-text, resolves action, narrates |
| `/api/play/context` | GET | Full game context for AI prompt building |
| `/api/whisper` | POST | Private message to a player |

### Discord Bot (`services/discord_bot.py`)
Full Discord integration running in a background thread alongside Flask. Auto-creates a set of game channels on `/setup`. Players link their accounts with `/join` + `/verify`.

**Slash commands available to players:**
`/action` · `/roll` · `/attack` · `/check` · `/cast` · `/save` · `/stats` · `/inventory` · `/join` · `/verify`

**DM slash commands:**
`/start` · `/reset` · `/play` (trigger AI DM turn) · `/narrate`

Bridges SMS ↔ Discord so both channels see the same game state in real time. Sends rich embeds for character sheets, combat order, and dice rolls.

### SMS Play Mode (`services/sms.py`, `sms_routes.py`)
Twilio integration allowing players to play entirely via text message. The AI DM (`services/ai_dm.py`) interprets player SMS messages, resolves game actions through the engine, and replies with narrated outcomes — no browser needed.

- Players register a phone number on the DM campaign page; receive a verification text
- Verified players text the Twilio number to perform any action
- AI DM engine handles ambiguous input ("I attack the goblin") and maps it to game mechanics
- DM can enable per-player **AI Agent mode** — the AI auto-plays that character's turn
- SMS ↔ Discord bridge keeps both channels in sync

### AI DM Engine (`services/engine.py`, `services/ai_dm.py`)
Pure-function game engine (`engine.py`) extracted from Flask route handlers — no session/flash/request dependencies, fully testable. Used by both the SMS AI DM and the Claude API `/api/play` endpoint.

`ai_dm.py` wraps the engine with an LLM layer: takes a player's free-text intent, constructs a rich game-context prompt, calls xAI Grok, and maps the response back to game actions (attack, skill check, narration, etc.).

### DM Settings Page (`/dm/settings`, `templates/dm/settings.html`)
In-app settings page for the DM to configure API keys without editing `.env` directly:
- Discord Bot Token + Client ID
- Claude API Key
- Twilio credentials
- Shows live Discord connection status

### Diagnostics Page (`/dm/diagnostics`, `templates/dm/diagnostics.html`)
Full system health dashboard with one-click tests for: environment variables, xAI Grok connectivity, Twilio SMS, AI engine, full pipeline (message → action → response), and Discord bot.

### Other Additions
- `/guide` — "How to Play" page for new players
- `/privacy` and `/terms` — legal pages
- `docker-compose.prod.yml` — production-ready compose config
- `CLAUDE.md` — project guide for AI-assisted development
- Sidebar nav updated: added ❓ How to Play and 🔧 Diagnostics links (DM)

---

### Bug Fixes & Incremental Improvements (Post-Phase 12)
- **QR code lazy render fix**: QR code in Campaign Info panel was not rendering because qrcodejs initialized against a hidden `<details>` element. Fixed by listening to the `details#campaign-info-details toggle` event and generating the QR code only when the panel is first opened.
- **xAI API key wiring**: Documented that `docker compose restart` does not re-read `env_file`; must use `docker compose up -d` to recreate the container and inject updated environment variables. `.env` file (gitignored) must be created from `.env.example` before AI features work.

### Phase 13: Sidebar Navigation & DM Impersonation Visibility
- **Objectives**: Replace the top nav bar with a left sidebar for better layout and discoverability; surface the DM impersonation ("View As") feature directly on the campaign page so it's not hidden behind the "Who's Online" widget.
- **Feedback source**: Playtest session — users reported a missing/hard-to-find navigation menu and DMs could not find the impersonation toggle.
- **Tasks**:
  1. **Sidebar Navigation** — Rework `base.html` to use a fixed left sidebar (~220px) instead of the top `<nav>` bar. Sidebar contains: brand logo, Dashboard, Characters, + Character, 📖 Rules, 📜 DM Guide (DM only), and a bottom-anchored user info + Logout block. Body layout becomes `display:flex` with the sidebar on the left and content area on the right.
  2. **Mobile collapse** — On narrow screens (<768px) the sidebar collapses to a hamburger icon that toggles a slide-in drawer.
  3. **DM Impersonation on Campaign Page** — Add "👁 View As" buttons next to each player listed in the Players section of the DM campaign page (not just in "Who's Online" on the dashboard). This makes the feature discoverable regardless of whether the player is currently online.
  4. **Impersonation banner polish** — Make the amber "DM View" banner more prominent; include the campaign name and a clearer call-to-action.
- **Deliverables**: Sidebar layout in `base.html`; mobile hamburger toggle; "View As" buttons on DM campaign page; improved impersonation banner.
- **Validation**: All pages render correctly with sidebar; DM can trigger impersonation from the campaign page; mobile view collapses gracefully.
- **Status**: Complete ✓ (top nav bar restored; left sidebar added alongside top nav with role-based sections — DM gets Campaigns, Characters, Rules, DM Guide; players get Campaigns, Characters, Rules only; sidebar hidden on <900px screens; "View As" button on DM campaign page styled gold; impersonation banner updated with clearer read-only warning)

### Phase 14: Character Assignment (DM Tool)
- **Objectives**: Allow the DM to reassign any character to any registered user — useful when a character is abandoned, pre-built by the DM, or needs to transfer between players.
- **Tasks**:
  1. Add `POST /dm/characters/<id>/assign` route — accepts `user_id` form field (empty = unassigned); DM-only; flashes confirmation.
  2. **Character sheet** — when viewed by a DM, show an "Ownership" card at the bottom: displays current owner, dropdown of all users, and an Assign button.
  3. **DM Dashboard** — in the "All Characters" list, show the current owner's username next to each character.
- **Deliverables**: Assign route; DM ownership panel on character sheet; owner label on DM dashboard character list.
- **Validation**: DM can reassign a character to any player; unassigned characters show "Unassigned"; owner label updates on dashboard.
- **Status**: Complete ✓ (POST /dm/characters/<id>/assign route; Ownership card on character sheet with dropdown of all users; owner label with ⚠ Unassigned indicator on DM dashboard All Characters list)

### Phase 15: Campaign Progress Tracker & Story Forks
- **Objectives**: Let the DM track where the party is in a structured campaign and model story branches/forks.
- **Tasks**:
  1. **Campaign Progress / Chapter Tracker**: Add a `chapters` list to `current_state`. Each chapter has a title, a description/summary, a status (`upcoming` / `active` / `completed`), and optional notes. DM can add, reorder, mark complete, and add notes to chapters from the campaign page.
  2. **Progress Panel**: Show a visual chapter timeline on the DM campaign page (and a read-only version for players) so everyone can see where they are in the story. The active chapter is highlighted; completed ones are checked off.
  3. **Story Forks**: Each chapter can have `branches` — named alternate paths (e.g. "Players follow the merchant" vs "Players investigate the cave"). The DM can create branches, pick the one the party took, and add notes per branch. Unchosen branches are greyed out but preserved so the DM can reference or reuse them.
  4. **AI-Assisted Chapter Summary**: An optional "Summarise this chapter" button (using xAI Grok) that reads the narration log entries since the chapter started and generates a short summary to pre-fill the chapter notes field.
- **Deliverables**: Chapter data model in `current_state`; DM chapter management UI; player progress view; story fork UI; AI chapter summary button.
- **Validation**: DM can create a 3-chapter adventure with a fork at chapter 2; marking chapter 1 complete updates the timeline; choosing a fork greys out the alternate branch.
- **Status**: Complete ✓ (2026-03-15)
- **Implementation Notes**:
  - `chapters` list added to `current_state` JSON; each chapter has `title`, `description`, `status`, `notes`, `summary`, `branches[]`, `active_branch`
  - Routes added: `POST /dm/campaigns/<id>/chapter/add`, `/chapter/<idx>/status`, `/chapter/<idx>/notes`, `/chapter/<idx>/delete`, `/chapter/<idx>/fork/add`, `/chapter/<idx>/fork/<i>/choose`, `/chapter/<idx>/summarize`
  - DM campaign page: visual chapter timeline card with status badges (upcoming/active/completed), per-chapter expand panel for notes + forks, story fork choose/add buttons, AI Summary button wired to xAI Grok
  - Player campaign page: read-only chapter timeline showing status, active fork, and AI-generated summaries
  - `summarize_chapter()` added to `services/ai.py` — reads chapter title, DM notes, and recent combat log entries for context
  - Fixed SQLite migration bug: `ALTER TABLE … ADD COLUMN … UNIQUE` is not supported; dropped UNIQUE constraint from `phone_number` migration

---

### Phase 16: Beta Playtest 1 Feedback — Combat UX & Quality of Life
- **Source**: `Feedback/Testing_3.md` — post-phase beta playtest 1 results (2026-03-15)
- **Note**: All AI features must continue to hide API keys in `.env` files; never commit keys to GitHub.
- **Objectives**: Address all 7 feedback items from the first beta session.
- **Tasks**:
  1. **Party visibility** — Add a "Party" panel to the player campaign page listing all other players in the campaign with their character name, class/level, and HP bar.
  2. **Attack target dropdown** — Replace the free-text "Target name" input on the player attack form with a `<select>` pre-populated from the current initiative order (when combat is active), with an "Other…" fallback option that reveals a custom text field.
  3. **DM NPC combat interface** — Add a collapsible "Roll Attack for NPC" mini-form under each NPC in the DM initiative order. Form fields: target (dropdown of PC combatants), attack bonus, damage dice. Rolls are posted to the combat log.
  4. **Combat turn guardrails** — Block the player attack and spell-cast actions (server-side) when combat is active and it is not that player's turn. Flash a clear error; redirect back. Free dice rolls and skill checks are not blocked.
  5. **DM revert combat log** — Add a "↩ Revert Last Entry" button next to the DM combat log header, backed by `POST /dm/campaigns/<id>/combat/log/revert` that pops the last entry.
  6. **HP visible without scrolling** — Show the active character's HP bar and current/max HP directly in the player campaign page header so it is always visible at the top.
  7. **Dice picker dropdowns** — Replace the free-text dice expression input with two dropdowns: count (1–6) and die type (d4 / d6 / d8 / d10 / d12 / d20). JavaScript assembles the expression string before submit.
- **Deliverables**: Updated `app.py` (routes + guards), updated `player/campaign.html`, updated `dm/campaign.html`.
- **Status**: Complete ✓ (2026-03-15)

---

### Phase 17: DM Campaign Page — Panel Consolidation & Collapsible Integrations
- **Source**: DM UX feedback (2026-03-17) — too many always-visible sections clutter the page.
- **Objectives**: Reduce visual noise on the DM campaign page without removing any functionality.
- **Tasks**:
  1. **Merge Getting Started + Campaign Info** — Permanent top card shows Join URL, large Join Code, Players Joined, QR code. A "Tell them how to get started" toggle button reveals/hides the 3-step walkthrough inline. Dismiss still persisted in state.
  2. **SMS Play Mode collapsible** — Wrap entire section in a `<details>` block. Summary shows title + a status pill (Active / Off). localStorage remembers open/closed state.
  3. **Discord Integration collapsible** — Same treatment: `<details>` with Connected / Not connected status pill.
- **Deliverables**: Updated `templates/dm/campaign.html` only.
- **Status**: Complete ✓ (2026-03-17)

---

### Phase 18: DM Campaign Page — Three-Button Accordion
- **Source**: DM UX feedback (2026-03-17) — consolidated panels still take too much vertical space; want three equal buttons that reveal content on demand.
- **Objectives**: Replace the three stacked cards (Campaign Info, SMS, Discord) with a compact three-button row. Clicking a button expands its panel below; clicking again collapses it. Only the content for the active panel is visible. Status indicators (Active / Off, Connected / Not connected, player count) visible on each button even when collapsed. Last open panel remembered via localStorage.
- **Deliverables**: Updated `templates/dm/campaign.html` only.
- **Status**: Complete ✓ (2026-03-17)

---

### Phase 19: Branding Integration — Campaign Codex Assets
- **Source**: New brand package uploaded 2026-03-17 (Branding/Logo/).
- **Objectives**: Apply the Campaign Codex visual identity across the app.
- **Tasks**:
  1. **Static asset setup** — Created `static/img/logo/`, `static/img/monogram/`, `static/img/icon/`, and `static/favicon/` directories. All brand files served by Flask at `/static/`.
     - `static/favicon/favicon.ico`, `favicon-16.png`, `favicon-32.png`, `apple-touch-icon.png`
     - `static/img/logo/campaign-codex-dark.png`, `campaign-codex-light.png`
     - `static/img/icon/codex-icon.png`, `codex-icon-1024.png`
     - `static/img/monogram/cc-monogram.png`, `cc-monogram-inverted.png`
  2. **Favicons** — Added `<link rel="icon">` tags in `base.html <head>` for all four favicon sizes. Updated page `<title>` to "Campaign Codex".
  3. **Nav bar brand** — Replaced plain text `⚔ D&D Manager` with `cc-monogram.png` (30px) + "Campaign Codex" text side by side, styled in gold.
  4. **Login page branding** — Added `campaign-codex-dark.png` logo above the login form; gold `border-color: var(--gold)` on the card; "Welcome Back / Sign in to continue your adventure" heading.
  5. **Sidebar brand** — Sidebar brand block removed after review; nav already shows monogram + text so sidebar was redundant.
- **Deliverables**: `static/` folder with all branding assets; updated `templates/base.html`; updated `templates/login.html`.
- **Status**: Complete ✓ (2026-03-17)

---

### Phase 20: Character Sheet — Official Layout + Background Tab + AI Generation
- **Source**: Beta playtest comparison against official D&D 5e character sheet layout (2026-03-17).
- **Objectives**: Add key missing sections so the character sheet is a complete reference during play, and empower players with AI-assisted backstory and personality generation.
- **Tasks**:
  1. **Temp HP** — display and edit field next to Current/Max HP. Stored in `character.spells['temp_hp']`. New route `POST /characters/<id>/temp_hp`.
  2. **Passive Scores** — show Passive Perception, Passive Investigation, Passive Insight (10 + skill modifier) as three labeled boxes. Computed server-side via inner `_passive()` helper in the character_sheet route.
  3. **Senses** — extract darkvision/tremorsense/etc. from race traits (filtering for sense keywords) and display as pills.
  4. **Languages** — pull from `race_data['languages']` and show in Proficiencies section.
  5. **Background Feature** — pull feature name from `BACKGROUNDS` data and show on sheet.
  6. **Tab interface** — reorganize bottom half into tabs: Saves & Skills | Inventory | Spells | Features | Background | Rests. All content preserved, just grouped more cleanly. Tab state persisted per-character via localStorage.
  7. **Background Tab** — new editable tab with: Custom Background textarea, Personality Traits, Ideals, Bonds, Flaws, Physical Characteristics grid (height, weight, age, eyes, hair, skin, gender), and Appearance textarea. All stored in `character.spells['background_details']` JSON. New route `POST /characters/<id>/background_details`.
  8. **AI Background Generation** — "✨ Clean Up" button polishes existing custom background text; "🎲 Generate" button creates a 2-4 paragraph origin story from character info. Both call xAI Grok via new routes.
  9. **AI Trait Generation** — "🎲 Generate" buttons on Personality Traits, Ideals, Bonds, and Flaws. Requires custom background to be filled in first (client-side guard alerts user if empty).
  10. **AI Appearance Generation** — "🎲 Generate" button on Appearance field. Requires both custom background AND at least one physical characteristic filled in.
- **New Routes**:
  - `POST /characters/<id>/temp_hp` — stores temp HP in `spells['temp_hp']`
  - `POST /characters/<id>/background_details` — stores 15 background fields in `spells['background_details']`
  - `POST /characters/<id>/ai/background/cleanup` — polish backstory via xAI Grok
  - `POST /characters/<id>/ai/background/generate` — generate origin story via xAI Grok
  - `POST /characters/<id>/ai/trait` — generate personality_traits / ideals / bonds / flaws (field specified in body)
  - `POST /characters/<id>/ai/appearance` — generate appearance description
- **New AI functions** (`services/ai.py`): `cleanup_background()`, `generate_background()`, `generate_trait_field()`, `generate_appearance()` — all return `(text, error)` tuple via `_call()`.
- **Auth helper**: `_char_ai_auth(char)` — allows character owner or DM to call AI routes.
- **Deliverables**: Updated `services/ai.py` (4 new functions), updated `app.py` (6 new routes + helper), updated `templates/character_sheet.html` (complete Background tab with AI buttons).
- **Status**: Complete ✓ (2026-03-17)

---

### Phase 21: DM Inspiration — Grant & Spend
- **Source**: DM request (2026-03-17) — DMs need a way to award Inspiration to players, just like adjusting HP.
- **Objectives**: Allow the DM to grant or revoke D&D Inspiration for any player character. Players can see their inspiration status on their character sheet and spend it.
- **D&D Rule**: Inspiration is a binary reward (have it or don't) that the DM awards for good roleplay. A player can spend it to gain advantage on any roll.
- **Tasks**:
  1. **Storage** — `character.spells['inspiration']` boolean. No migration needed.
  2. **DM toggle route** — `POST /dm/characters/<id>/inspiration`: flips the boolean, flashes confirmation, redirects back to campaign.
  3. **DM campaign page** — Add a "★ Grant Inspiration" / "★ Revoke Inspiration" toggle button below the HP adjust form for each player's character in the Players section.
  4. **Character sheet pill** — Add an Inspiration pill in the combat-bar row. Shows "★ Inspired!" in gold when active, "☆ No Inspiration" in muted when not. If `can_edit`, shows a "Spend" button when inspired.
  5. **Spend route** — `POST /characters/<id>/inspiration/spend`: clears inspiration (player or DM), flashes confirmation.
- **Deliverables**: Two new routes in `app.py`; updated `templates/dm/campaign.html`; updated `templates/character_sheet.html`.
- **Status**: Complete ✓ (2026-03-17)

---

### Phase 22: Campaign Markdown v2 — Chapters, Scene & Dialogue Import
- **Source**: Gap identified between the Example `.md` file and the saved `.json` — chapters and NPC scene/dialogue data were lost on import (2026-03-18).
- **Objectives**: Close the round-trip between a campaign `.md` file and a fully-loaded campaign, so chapters, NPC scenes, and DM dialogue survive import.
- **Root causes**:
  1. `parsers.py` only read single-line `Notes:` — NPC `Scene` and `Dialogue` blocks had no parseable home
  2. No `## Chapters` section in v1 `.md` — chapters existed only in the JSON save, not in the importable template
  3. `campaign_import()` in `app.py` never populated `current_state['chapters']`
- **Tasks**:
  1. **`_multiline_field(body, key, known_fields)`** — new helper in `parsers.py` that captures field values
     spanning multiple lines, terminating at the next known field name.
  2. **NPC `Scene:` and `Dialogue:` fields** — each NPC block now supports separate `Scene:` and `Dialogue:`
     fields (multiline). Parser extracts them and combines into rich `notes` with `SCENE:` and `DIALOGUE:`
     labels, fully compatible with the existing NPC preset display.
  3. **`_parse_chapters(text)`** — new function that reads a `## Chapters` section. Each chapter uses
     `### Chapter: Title` with `Description:` (multiline), `Status:`, `Notes:` (multiline), and one or
     more `Branch:` lines. Returns a list of chapter dicts matching the Phase 15 chapter tracker schema.
  4. **`parse_campaign_md` updated** — returns `chapters` list in addition to existing fields. Backwards
     compatible: campaigns without a `## Chapters` section return an empty list.
  5. **v1 compatibility** — NPC parser skips `### CHAPTER X —` divider headers that appear in v1 files.
  6. **`campaign_import()` updated** — threads `chapters` into `current_state`. Flash message now reports
     NPC count and chapter count separately.
  7. **`CAMPAIGN_TEMPLATE` updated** — new v2 format shows `## Chapters` section with 3 example chapters
     plus NPCs with `Scene:` and `Dialogue:` fields.
  8. **`Examples/LostMinesOfPhandelver_Campaign_v2.md`** — full v2 conversion: all 4 chapters with
     descriptions, DM notes, and 2 named branches each; all NPCs with separate Scene and Dialogue fields.
- **Deliverables**: Updated `parsers.py`; updated `app.py`; new `Examples/LostMinesOfPhandelver_Campaign_v2.md`.
- **Status**: Complete ✓ (2026-03-18)

---

### Phase 23: Character & Campaign Download Templates — v2 Format
- **Source**: Review of download templates after Phase 22 (2026-03-19) — CHARACTER_TEMPLATE was still v1
  (no background/story fields); CAMPAIGN_TEMPLATE was already updated in Phase 22.
- **Objectives**: Bring the character download template up to date with Phase 20 character sheet additions
  so players can fully specify their character — including backstory, personality, and physical description
  — in the markdown file they import. What you write in the template becomes immediately usable by the
  AI generation features on the character sheet.
- **Tasks**:
  1. **`CHARACTER_TEMPLATE` v2** — add five new sections after `## Gold`:
     - `## Physical Characteristics` — Height, Weight, Age, Eyes, Hair, Skin, Gender (key-value)
     - `## Backstory` — freeform multi-line origin story (feeds AI generation)
     - `## Personality Traits` — freeform (feeds AI trait generation)
     - `## Ideals` — freeform
     - `## Bonds` — freeform
     - `## Flaws` — freeform
     - `## Appearance` — freeform physical description
     - Added comment header explaining the file format
  2. **`parse_character_md` v2** — reads all seven new sections using `_section()` and `_kv()`.
     Returns `physical` dict + `custom_background`, `personality_traits`, `ideals`, `bonds`, `flaws`,
     `appearance` strings alongside existing fields. Fully backwards-compatible with v1 templates.
  3. **`character_import()` updated** — builds `bg_details` dict from all new parsed fields and stores
     it in `spells['background_details']` at character creation time. No migration needed — the
     background_details key is already handled by the character sheet route.
- **Not changed**: `CAMPAIGN_TEMPLATE` (already v2 from Phase 22). Parser for campaigns is unchanged.
- **Deliverables**: Updated `parsers.py` (template + parser); updated `app.py` (import route).
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 24: AI Character Generator Wizard
- **Source**: DM/player request (2026-03-19) — "New Character" should offer an AI-powered path alongside manual creation.
- **Objectives**: Build a full AI character generation wizard with a preview/approval step so no character is created without the player's sign-off.
- **User flow**:
  1. `/characters/new` — two-path choice: "🎲 Generate with AI" or "✏️ Create Manually"
  2. `/characters/generate` (GET) — wizard form: Race, Class, Background, Alignment (required); Name Hint + 4 story prompt textareas (all optional)
  3. `/characters/generate` (POST) — validates inputs, calls xAI Grok, stores result in session, redirects to preview
  4. `/characters/generate/preview` — full character preview: name in gold, identity pills, ability score grid (standard array assigned by AI priority), backstory, personality traits/ideals/bonds/flaws (2×2 grid), appearance; three action buttons
  5. `/characters/generate/confirm` (POST) — creates Character in DB with `background_details` fully populated from AI output; redirects to character sheet
  6. `/characters/generate/regenerate` (POST) — re-calls AI with same inputs from session, shows new preview; no data is lost
- **AI function**: `generate_character(race, class_name, background, alignment, name_hint, prompts)` in `services/ai.py`
  - System prompt instructs Grok to return ONLY valid JSON (no fences) with keys: name, backstory, personality_traits, ideals, bonds, flaws, appearance, ability_priorities (ordered list of 6 ability score abbreviations), suggested_skills
  - `max_tokens=1400` (up from 600 via new `_call(messages, max_tokens=600)` default parameter)
  - Response parsed with `json.loads()`; markdown fences stripped if present; ability_priorities validated/deduped/padded
- **Ability score assignment**: AI returns priority order → standard array `[15,14,13,12,10,8]` assigned in that order → racial ASI applied on top
- **Skill assignment**: AI's suggested_skills filtered to class options; remaining class slots filled automatically from available class skills
- **`_call()` updated**: added `max_tokens=600` default parameter — backwards-compatible with all existing callers
- **Session storage**: `session['char_gen']` holds `{result, inputs}` across the preview and regenerate steps; cleared on confirm
- **New files**: `templates/character_generate.html`, `templates/character_preview.html`
- **Updated files**: `services/ai.py`, `app.py`, `templates/character_create.html`
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 25: AI Player Character Flagging & Identity
- **Source**: DM request (2026-03-19) — DM wants to assign AI control to player characters so they can practice DMing against simulated players.
- **Objectives**: Give the DM a way to mark any character as AI-controlled and set its persona level (novice / intermediate / experienced); surface this clearly in the UI so the DM always knows which characters are human vs AI.
- **Data model** (no schema change — stored in existing `character.spells` JSON):
  - `spells['ai_player']` — boolean, default `False`
  - `spells['ai_level']` — string: `"novice"` | `"intermediate"` | `"experienced"`, default `"intermediate"`
- **DM UI additions** (`templates/dm/campaign.html`, Players section):
  - Below the existing HP-adjust form and inspiration toggle for each character: new "AI Player" row
  - Toggle button: "🤖 Enable AI" / "✅ AI Active — Disable" — calls `POST /dm/characters/<id>/ai-toggle`
  - When AI is active: persona level selector appears — three buttons (Novice / Intermediate / Experienced), active one highlighted in gold; calls `POST /dm/characters/<id>/ai-level`
- **Character sheet badge** (`templates/character_sheet.html`):
  - If `ai_player` is True: subtle "🤖 AI-Controlled" badge in the character header area (muted style, not intrusive)
- **Campaign page badge** (`templates/dm/campaign.html`):
  - Character name in Players section gets a small `[🤖 Novice]` / `[🤖 Experienced]` tag next to it when AI is active
- **New routes** (`app.py`):
  - `POST /dm/characters/<id>/ai-toggle` — flips `spells['ai_player']`; DM-only; redirects back to campaign
  - `POST /dm/characters/<id>/ai-level` — sets `spells['ai_level']` to posted value (`novice`/`intermediate`/`experienced`); DM-only; redirects back to campaign
  - Both routes use `flag_modified(char, 'spells')` after mutation
- **Updated files**: `app.py`, `templates/dm/campaign.html`, `templates/character_sheet.html`
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 26: AI Player Out-of-Combat Actions
- **Source**: DM request (2026-03-19) — AI-flagged characters should be able to generate contextually appropriate player actions during narrative/exploration scenes.
- **Objectives**: DM can trigger an AI action for any AI-flagged character; the AI generates what that character would say or do based on their persona level; DM previews and optionally edits before posting to the campaign log.
- **Prerequisites**: Phase 25 complete.
- **New file** `services/ai_player.py`:
  - `generate_player_action(character, campaign, persona_level)` — main function
  - Builds context from: character name/race/class/background, personality traits/ideals/bonds/flaws (from `background_details`), recent narration log (last 5 entries from `current_state['narration_log']`), current scene description
  - Persona-level system prompt modifiers:
    - **Novice**: "You are roleplaying as a first-time tabletop RPG player. Your character speaks simply and directly. You often ask the DM clarifying questions. You sometimes forget to use skills or abilities. You focus on obvious actions rather than creative solutions."
    - **Intermediate**: "You are roleplaying as a player with some experience. Your character uses their backstory occasionally to inform decisions. You use skills and abilities when clearly relevant. You engage with NPCs and plot hooks."
    - **Experienced**: "You are roleplaying as a veteran RPG player. Your character has a distinct voice, references past events, and makes mechanically efficient choices. You look for creative solutions, ask probing questions of NPCs, and use all available tools."
  - Returns `(action_text, error)` — plain narrative string of what the character does/says
- **DM UI additions** (`templates/dm/campaign.html`, Players section):
  - For each AI-flagged character: "🎲 Take Action" button appears below the inspiration toggle
  - Clicking opens a small form: text field pre-filled with current scene context (editable), "Generate" button
  - `POST /dm/characters/<id>/ai-action` returns the generated action text
  - DM sees action in a preview card with character name and persona level badge
  - Three buttons: "✅ Post to Log" (saves to narration_log), "✏️ Edit & Post" (editable textarea + post), "❌ Discard"
  - "All AI Players" batch trigger at top of Players section — generates actions for all AI characters sequentially, queues them for DM approval
- **New routes** (`app.py`):
  - `POST /dm/characters/<id>/ai-action` — calls `generate_player_action()`, returns JSON `{action, character_name, persona_level}`
  - `POST /dm/characters/<id>/ai-action/post` — accepts `{action_text}`, appends to `current_state['narration_log']`
- **Updated files**: `app.py`, `templates/dm/campaign.html`
- **New files**: `services/ai_player.py`
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 27: AI Player Combat Decisions
- **Source**: DM request (2026-03-19) — AI players should participate in combat rounds, not just narrative scenes.
- **Objectives**: When it is an AI character's turn in combat, the DM can trigger an AI decision; the AI picks a target, action, and (if applicable) spell or bonus action; the DM approves before the engine executes it.
- **Prerequisites**: Phase 25 complete; Phase 26 `services/ai_player.py` in place.
- **New function** `generate_combat_decision(character, campaign, persona_level)` in `services/ai_player.py`:
  - Context fed to the AI: character stats (HP, AC, spell slots, conditions), initiative order, all combatants with current HP, recent combat log (last 3 rounds), terrain notes from `current_state`
  - AI returns a structured JSON decision: `{action_type, target, weapon_or_spell, bonus_action, reasoning}`
  - Persona shapes decision style:
    - **Novice**: may attack the nearest enemy regardless of tactics; may forget bonus actions; might use a powerful spell on a weak target
    - **Intermediate**: picks reasonable targets (lowest HP or biggest threat); uses bonus actions; conserves spell slots until badly needed
    - **Experienced**: optimal focus-fire, uses action economy efficiently, coordinates with party (e.g., avoids attacking an ally's Hold Person target)
  - Returns `(decision_dict, error)` — same pattern as `generate_character()`
- **DM UI additions** (`templates/dm/campaign.html`, combat section):
  - When combat is active and it is an AI character's turn: "🤖 AI Turn" button appears next to that character's initiative slot
  - Clicking "🤖 AI Turn" calls `POST /dm/characters/<id>/ai-combat-turn`
  - Response displays the AI's proposed decision in a modal or inline card: "Thordak attacks Goblin A with Greataxe — reasoning: lowest HP, within range"
  - DM buttons: "✅ Execute", "✏️ Edit Action", "⏭ Skip Turn"
  - On "Execute": calls existing engine routes (`/dm/characters/<id>/attack`, etc.) with the AI-chosen parameters
- **New routes** (`app.py`):
  - `POST /dm/characters/<id>/ai-combat-turn` — calls `generate_combat_decision()`, returns JSON decision for DM review
  - `POST /dm/characters/<id>/ai-combat-execute` — receives approved decision dict, routes to correct engine function, returns result
- **Updated files**: `services/ai_player.py`, `app.py`, `templates/dm/campaign.html`
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 28: Practice Mode — Full-Party AI Orchestration
- **Source**: DM request (2026-03-19) — DM wants to run complete practice sessions where every player slot is AI-controlled.
- **Objectives**: Let the DM "advance" the entire party with one action, mix AI personas across characters, step in as any character mid-session, and get a post-session summary they can learn from.
- **Prerequisites**: Phases 25, 26, 27 complete.
- **DM UI additions** (`templates/dm/campaign.html`):
  - "🎓 Practice Mode" toggle button at the top of the campaign panel — only enabled when all active characters have `ai_player: true`
  - When Practice Mode is active: banner at top of page ("Practice Mode Active — All characters are AI-controlled"); "⏭ Advance Party" button
  - "⏭ Advance Party" — triggers all AI characters in turn order (combat or narrative) in sequence, showing each decision for DM review before execution; DM can skip, edit, or approve each one
  - "Hot Seat" button per character — DM temporarily overrides AI for that character and types their own action; one action only, then AI resumes
- **Session summary** (new route `GET /dm/campaigns/<id>/practice-summary`):
  - Shows a recap of the session: actions taken, rolls made, outcomes; which persona made which decision
  - AI-generated debrief: what each AI "player" did well, what a real player might have done differently
  - Useful for DM skill-building — see how players of different experience levels think
- **Persona mixing**: DM can assign different levels (novice/intermediate/experienced) to different characters; Practice Mode respects each character's individual level
- **Difficulty awareness**: The AI debrief notes when decisions were suboptimal (e.g., novice walking into a trap a veteran would have spotted) — helps DM understand player experience gaps
- **New route**: `POST /dm/campaigns/<id>/advance-party` — iterates all AI characters, calls `generate_player_action()` or `generate_combat_decision()` for each, returns ordered list of pending decisions; DM approves/edits/skips each via existing Phase 26/27 confirm routes
- **New template**: `templates/dm/practice_summary.html`
- **Updated files**: `templates/dm/campaign.html`, `app.py`
- **Status**: Complete ✓ (2026-03-19)

---

### Phase 29: Admin Console — User & Account Management
- **Source**: DM request (2026-03-20) — user forgot their password; need an admin panel to manage accounts without touching the database directly.
- **Objectives**: Give a designated super-admin a web UI to view, manage, and troubleshoot all user accounts.
- **Prerequisites**: Phase 1 (auth/users) complete.
- **Admin role**: Add `is_admin` boolean field to `User` model (default `False`). Seed one admin via env var `ADMIN_EMAIL` on first run or via a CLI command `flask create-admin`.
- **Admin-only routes** (all behind `@admin_required` decorator):
  - `GET /admin` — dashboard: total users, campaigns, characters, recent signups
  - `GET /admin/users` — paginated user list: username, email, role (DM/player/admin), last login, account status (active/banned)
  - `GET /admin/users/<id>` — user detail: profile info, linked characters, campaigns, login history
  - `POST /admin/users/<id>/reset-password` — generate a temporary one-time password and display it to admin (user must change on next login)
  - `POST /admin/users/<id>/toggle-ban` — ban/unban account (banned users get "Account suspended" on login)
  - `POST /admin/users/<id>/set-role` — promote to DM, demote to player, or grant admin
  - `DELETE /admin/users/<id>` — soft-delete: mark `deleted_at`, anonymize PII, orphan characters (don't cascade-delete campaign data)
  - `POST /admin/users/<id>/send-reset-email` — trigger password reset email (requires email config)
- **Admin UI** (`templates/admin/`):
  - `base.html` — admin layout: sidebar nav (Dashboard, Users, Campaigns, Characters, System)
  - `dashboard.html` — stats cards + recent activity feed
  - `users.html` — searchable/filterable table with inline actions
  - `user_detail.html` — full profile with action buttons
- **Security**: Admin routes require both `@login_required` and `@admin_required`; all actions logged to an `AdminAuditLog` table (who did what, when, to whom)
- **Updated files**: `models.py`, `app.py`, `templates/admin/*.html`
- **Status**: Complete ✓ (2026-03-20)

---

### Phase 30: Admin Console — Campaign & Character Oversight
- **Source**: Natural extension of Phase 29 — admins should be able to inspect and fix campaign/character state without direct DB access.
- **Objectives**: Full CRUD visibility over campaigns and characters; ability to reassign ownership, fix broken state, and export data.
- **Prerequisites**: Phase 29 complete.
- **Campaign management**:
  - `GET /admin/campaigns` — all campaigns: name, DM, player count, status (active/archived), created date
  - `GET /admin/campaigns/<id>` — full campaign detail: players, characters, `current_state` JSON viewer, narration log, combat log
  - `POST /admin/campaigns/<id>/reassign-dm` — transfer DM ownership to another user
  - `POST /admin/campaigns/<id>/reset-state` — wipe `current_state` back to defaults (nuclear option for broken sessions)
  - `POST /admin/campaigns/<id>/archive` — soft-archive (hidden from active list, data preserved)
  - `GET /admin/campaigns/<id>/export` — download full campaign JSON (all logs, characters, state)
- **Character management**:
  - `GET /admin/characters` — all characters: name, class, level, owner, campaign assignment
  - `GET /admin/characters/<id>` — full character detail: stats, spells JSON viewer, HP, conditions
  - `POST /admin/characters/<id>/reassign` — move character to a different user or campaign
  - `POST /admin/characters/<id>/fix-hp` — admin override to set current/max HP (for data corruption)
  - `DELETE /admin/characters/<id>` — hard delete (with confirmation prompt)
- **JSON state viewer**: Collapsible read-only JSON tree for `current_state` and `spells` fields — lets admin inspect without raw DB access
- **Audit trail**: All campaign/character admin actions logged to `AdminAuditLog`
- **Updated files**: `app.py`, `templates/admin/campaigns.html`, `templates/admin/campaign_detail.html`, `templates/admin/characters.html`, `templates/admin/character_detail.html`
- **Status**: Complete ✓ (2026-03-20)

---

### Phase 31: Admin Console — System Health & Diagnostics
- **Source**: Ops need — as the app grows, the admin needs visibility into system health, errors, and API usage.
- **Objectives**: System-level dashboards for monitoring, error triage, and API key management — all without SSH access.
- **Prerequisites**: Phase 29 complete.
- **System dashboard** (`GET /admin/system`):
  - App version, uptime, Python/Flask versions
  - Database stats: total rows per table, DB file size (SQLite), recent slow queries
  - Active sessions count (users logged in last 30 min)
  - Disk usage: `instance/` folder size, log file sizes
- **Error log viewer** (`GET /admin/logs`):
  - Tail of `app.log` (last 200 lines) with auto-refresh toggle
  - Filter by level: ERROR, WARNING, INFO
  - Download full log file button
- **AI API usage tracker**:
  - Log each xAI API call: timestamp, character/campaign, tokens used, latency, success/failure
  - `GET /admin/ai-usage` — table of recent calls + daily token totals
  - Helps spot runaway usage or API key exhaustion early
- **Discord bot status** (`GET /admin/discord`):
  - Bot online/offline indicator (ping the Discord API)
  - Last command run, command usage counts
  - "Restart Bot" button (sends SIGTERM to bot process, supervisor restarts it)
- **Password reset email config** (`GET/POST /admin/settings`):
  - SMTP settings (host, port, from address) stored in DB — no restart needed to change
  - Test email button
- **Updated files**: `services/ai.py` (usage ring buffer), `app.py`, `templates/base.html`, `templates/admin/system.html`, `templates/admin/logs.html`, `templates/admin/ai_usage.html`
- **Note**: AI usage tracked in-memory (deque of 500 calls in `services/ai.py`) — no DB model needed; resets on restart which is acceptable for operational monitoring. SMTP config deferred (no email infrastructure in place).
- **Status**: Complete ✓ (2026-03-20)

---

### Phase 32: AI Combat Execution — Dice Rolls & DM Roll-for-Character
- **Source**: DM request (2026-03-20) — AI combat decisions were planned but execution (rolling dice, applying results) was still manual.
- **Objectives**: When a DM approves an AI combat decision, the engine should automatically roll dice and apply the result; DMs should also be able to roll on behalf of any character (player or NPC) directly from the combat panel.
- **Tasks**:
  1. **AI combat execute route** — `POST /dm/characters/<id>/ai-combat-execute` resolves the approved AI decision through the game engine (attack roll, damage, spell effect), logs to the combat log, and returns the result narrative.
  2. **DM roll-for-character** — mini-form in the DM initiative panel allowing the DM to roll any die (or expression) on behalf of a specific combatant; result appended to the combat log with the character's name.
  3. **Scroll persistence on form submit** — DM campaign page saves scroll position to `sessionStorage` before form submission and restores it on load so the DM's view doesn't jump to the top after every action.
- **Updated files**: `app.py`, `templates/dm/campaign.html`
- **Status**: Complete ✓ (2026-03-20)

---

### Phase 33: Remove Combatants from Combat Mid-Scene
- **Source**: DM request (2026-03-20) — DMs needed a way to pull a character or NPC out of the initiative order during combat (fled, incapacitated, no longer relevant) without ending the whole encounter.
- **Objectives**: Add a per-combatant "Remove" action in the DM's initiative panel that removes that combatant from the order and adjusts the turn pointer if needed.
- **Tasks**:
  1. `POST /dm/campaigns/<id>/combat/remove` — accepts a `combatant_name` form field; removes the combatant from `current_state['initiative_order']`; adjusts `current_turn` index if the removed slot was at or before the current pointer; logs a combat log entry.
  2. DM campaign page — "✕ Remove" button next to each combatant in the initiative order list.
  3. Guard: if removing the last combatant, treat it as combat end (same as the existing end-combat route).
- **Updated files**: `app.py`, `templates/dm/campaign.html`
- **Status**: Complete ✓ (2026-03-20)

---

### Phase 34: Player Page — Section State Persistence (Skill Check & Attack Roll)
- **Source**: Player bug report (2026-03-21) — Skill Check and Attack Roll sections collapse back to their default state on every page refresh, causing friction mid-session.
- **Objectives**: Persist the expanded/collapsed state of every `<details>` section on the player campaign page across refreshes and auto-reloads using `localStorage`.
- **Root cause**: All action sections use the HTML `<details>` element whose open/closed state is purely in-memory and resets on any navigation or `location.reload()`.
- **Sections affected** (all in `templates/player/campaign.html`):
  - Roll Dice (line ~146) — starts open, collapses if user closes it
  - **Skill Check** (line ~176) — reported bug; starts closed
  - **Attack Roll** (line ~198) — reported bug; partially driven by `is_my_turn` but user toggle is lost
  - Cast Spell (line ~249) — starts closed
  - Quick Reference (line ~410) — starts closed
  - Scene Earlier History (line ~101) — starts closed
- **Tasks**:
  1. Add a `data-persist-key` attribute to each `<details>` element on the player campaign page (e.g., `data-persist-key="player_details_skill_check"`).
  2. Add a small JavaScript block (bottom of page) that:
     - On page load: reads each key from `localStorage` and sets `details.open = true` if stored as `"1"`.
     - On every `toggle` event on a `<details>` element: writes `"1"` or `"0"` to `localStorage` under that key.
  3. For Attack Roll: if `is_my_turn` is true server-side, override the stored state and force-open the section (so it still auto-opens on a player's turn even if they had it collapsed before).
  4. Key namespace: `player_<campaign_id>_<section_name>` to avoid conflicts across campaigns.
- **Deliverables**: Updated `templates/player/campaign.html` only — no backend changes.
- **Validation**: Open Skill Check section → refresh → section stays open. Close Roll Dice → refresh → stays closed. Start combat as active player → Attack Roll opens automatically regardless of prior state.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 35: Player Page — Form Field State Persistence
- **Source**: Same bug report session (2026-03-21) — form inputs reset on page refresh, frustrating players who are mid-action.
- **Objectives**: Persist player action form field selections in `localStorage` so they survive the 20-second auto-refresh and manual reloads.
- **Fields affected** (all in `templates/player/campaign.html`):
  - Dice count & die type dropdowns (Roll Dice form)
  - Skill selection dropdown (Skill Check form)
  - Target dropdown + custom target text field, AC input, ability dropdown, damage dice inputs (Attack Roll form)
  - Spell name, slot level, concentration checkbox (Cast Spell form)
- **Auto-refresh interaction**: The page calls `location.reload()` every 20 seconds. Form state must be saved **before** the reload fires and restored immediately after page load — not just on user interaction.
- **Tasks**:
  1. Write a `persistField(el, key)` helper that:
     - On `change` / `input`: saves value to `localStorage[key]`.
     - Saves state also immediately before `location.reload()` is called (intercept the reload call or add a `beforeunload` / pre-reload save flush).
  2. On page load: for each persisted field, read `localStorage` and set the element's value before the page renders visually.
  3. Restore the Attack Roll "Other…" custom target input display state (show/hide) based on the saved target dropdown value.
  4. Clear persisted form state when a form is **successfully submitted** (listen for the form's `submit` event; on submit, delete the relevant keys so stale data doesn't re-appear after an action completes).
  5. Key namespace: `player_<campaign_id>_form_<field_name>`.
- **Deliverables**: Updated `templates/player/campaign.html` only — no backend changes.
- **Validation**: Fill in Attack Roll form → page auto-refreshes (20 s) → all fields still populated.
- **Implementation notes**: Fields persisted: dice count/type, skill selection, attack ability, damage dice, target AC, spell name, slot level, concentration. Target `<select>` and custom target text are intentionally skipped — the target dropdown is server-rendered from initiative order (dynamic) and restoring a stale selection is confusing. "Clear on submit" was also dropped: players often repeat the same attack setup, so persistence across submits is a better UX, and the target dropdown options naturally refresh from the server each reload.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 36: DM Page — Panel & Section State Persistence
- **Source**: Discovered during player bug audit (2026-03-21) — DM page has many toggle panels and `<details>` sections whose visibility resets on refresh, forcing DMs to re-open sections after every page load.
- **Objectives**: Persist the open/closed state of every DM-side panel and `<details>` section using `localStorage` (building on the existing partial implementation for the top accordion and Getting Started toggle).
- **Sections / panels affected** (all in `templates/dm/campaign.html`):
  - AI Player Action form (currently toggled via `toggleAiForm()` JS — no localStorage)
  - AI Combat Result panel (shown by `triggerAiCombatTurn()`)
  - Hot Seat form panel (`toggleHotSeat()`)
  - Load Campaign File panel (inline `onclick` toggle)
  - AI Action Edit panel (`editAiAction()`)
  - SMS Log `<details>` block (line ~457)
  - Per-character Conditions `<details>` blocks (one per player, lines ~741, ~765)
  - Narration text `<details>` (line ~971+)
- **Tasks**:
  1. For each `<details>` element: add `data-persist-key` attribute; attach the same `toggle` listener pattern from Phase 34.
  2. For JS-toggled panels (`toggleAiForm`, `toggleHotSeat`, Load File): wrap the existing show/hide logic to also write to `localStorage`; on page load, read and apply.
  3. Per-character condition sections: key includes the character ID so each player's section is tracked independently (e.g., `dm_<campaign_id>_conditions_<char_id>`).
  4. Panels that are **ephemeral by nature** (AI Combat Result, AI Action Edit preview) should NOT be persisted — they show transient AI-generated content that is meaningless after a reload. Skip these.
  5. Key namespace: `dm_<campaign_id>_<section_name>`.
- **Deliverables**: Updated `templates/dm/campaign.html` only — no backend changes.
- **Validation**: Open SMS Log section → refresh → still open. Open Hot Seat form → refresh → still open. Close each per-character conditions panel individually → refresh → each remembers its state.
- **Implementation notes**: Used `data-persist-key` attribute pattern on all `<details>` elements — a single generic JS listener picks them all up. Ephemeral panels (AI Combat Result, AI Action Edit, AI Player result card) intentionally not persisted. Load panel and Hot Seat panels use localStorage-aware toggle functions. Keys are namespaced `dm_<campaign_id>_<section>`.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 37: DM Page — Form Field State Persistence
- **Source**: Discovered during player bug audit (2026-03-21) — DM textareas and combat form inputs reset on refresh, causing DMs to lose in-progress AI hints, hot-seat text, and HP adjustments.
- **Objectives**: Persist DM form inputs that represent work-in-progress across page refreshes.
- **Fields affected** (all in `templates/dm/campaign.html`):
  - AI Hint textarea (scene context for AI player actions, line ~48–50)
  - Hot Seat textarea (DM action text, line ~26–28)
  - AI Action Edit textarea (edited AI action text, line ~86–87) — **ephemeral, skip**
  - Per-combat HP Adjust input (line ~731)
  - Condition type and target dropdowns (lines ~750, ~774)
  - Attack bonus, target AC, damage dice inputs in DM attack roll mini-form (lines ~785, ~789, ~793)
- **Tasks**:
  1. AI Hint and Hot Seat textareas: persist on `input` event; restore on page load. Clear on successful form submit.
  2. Combat HP Adjust and attack roll fields: persist per-character using key `dm_<campaign_id>_combat_<char_id>_<field>`. Clear when combat ends (detect from `current_state.combat_active === false` passed as a JS variable from Flask).
  3. Condition selects: persist the last-used condition type and target as defaults for convenience (not cleared on submit — DMs often apply the same condition repeatedly).
  4. Skip AI Edit textarea — its content is generated fresh each time and stale content would be confusing.
  5. Key namespace: `dm_<campaign_id>_form_<section>_<field>`.
- **Deliverables**: Updated `templates/dm/campaign.html` only — no backend changes.
- **Validation**: Type in narration textarea → refresh → text still there. Submit narration → textarea clears. Open Hot Seat, type action → refresh → panel still open, text preserved. Submit hot seat post → panel closes and text clears.
- **Implementation notes**: Used `data-persist-key` attribute on textareas — same generic JS listener as Phase 36 picks them all up. HP adjust inputs and combat roll inputs (atk bonus, target AC, damage dice) were skipped — they are single-number entries that DMs type in seconds and stale values would be confusing. Condition selects also skipped — the full form is rarely left mid-entry. AI Edit textarea intentionally skipped (ephemeral). Narration textarea is cleared on narrate form submit. Hot seat textareas are cleared on their post form submit.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 38: Player Narration Submissions
- **Source**: Player request (2026-03-21) — players want to post what their character does directly to the narration log, just like the DM narrates scenes.
- **Objectives**: Give players a "Post to Story" form on their campaign page so they can contribute in-character actions and dialogue to the shared narration log.
- **Data change**: Add an `author` field to every narration log entry (`"author": "DM"` for existing DM posts, `"author": "<character name>"` for player posts). Backwards-compatible — existing entries without `author` render as DM posts.
- **Tasks**:
  1. **New route** `POST /player/campaigns/<id>/narrate` — accepts `narration` text field; guards that the campaign is active and the player has a character; prepends `"<CharName>: "` label to the text; appends to `current_state['narration_log']` with `author` set to the character's name; redirects back.
  2. **Player campaign page** — add a "Post to Story" form below the Actions card: a `<textarea>` with character name prefix label, a submit button. Keep it visually lighter than the DM's narration form so the hierarchy is clear (DM sets scenes; players react within them).
  3. **Narration log rendering** (both DM and player pages) — display the `author` field next to each timestamp so everyone can see who posted each entry. DM posts render in gold; player posts render with the character name in a muted blue/white.
  4. **Guard**: player narration does NOT consume a spell slot, HP, or any game resource — it is purely flavour text. Server enforces this by using the narrate route, not any action route.
- **New routes**: `POST /player/campaigns/<id>/narrate`
- **Updated files**: `app.py`, `templates/player/campaign.html`, `templates/dm/campaign.html`
- **Validation**: Player posts "Aldric raises his lantern and peers into the darkness." → entry appears in the narration log on both DM and player views, labelled "Aldric" in a distinct colour. DM's existing narrations still render correctly without the author label (fallback to "DM").
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 39: DM Narration Log Management — Revert & Delete
- **Source**: DM request (2026-03-21) — DMs need a way to undo mistakes or remove inappropriate player narration entries, just like the existing combat log revert.
- **Objectives**: Give the DM a "Revert Last" button to pop the most recent entry, and a per-entry delete button for surgical removal anywhere in the log.
- **Tasks**:
  1. **Revert last** — `POST /dm/campaigns/<id>/narration/revert`: pops `current_state['narration_log'][-1]`; flashes what was removed; redirects back. Add a "↩ Revert Last" button next to the Narration Log header on the DM campaign page (same pattern as the combat log revert from Phase 16).
  2. **Delete specific entry** — `POST /dm/campaigns/<id>/narration/delete`: accepts an `entry_idx` (integer index into the log); removes that entry; redirects back. Add a small "✕" button next to each narration log entry on the DM view only (not shown to players).
  3. **Guard**: Both routes are DM-only (`@dm_required`). Index bounds are validated server-side to prevent out-of-range deletes.
- **New routes**: `POST /dm/campaigns/<id>/narration/revert`, `POST /dm/campaigns/<id>/narration/delete`
- **Updated files**: `app.py`, `templates/dm/campaign.html`
- **Validation**: Post a narration → click "↩ Revert Last" → entry disappears from log on both pages. Post three entries → click ✕ on the middle one → only that entry is removed, the other two remain in order.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 40: Player AI Narration Assistance
- **Source**: Player request (2026-03-21) — players want the same AI writing help the DM has: a "Clean Up" button to polish their draft and a "Generate" button to get an in-character action suggestion based on the current scene.
- **Objectives**: Add AI-assisted narration buttons to the player's "Post to Story" form.
- **Prerequisites**: Phase 38 complete (player narrate form exists).
- **Tasks**:
  1. **`POST /player/campaigns/<id>/ai/narration/cleanup`** — takes the player's draft text from the request body; calls `services/ai.py` with a prompt instructing Grok to refine it in the character's voice (using name, race, class, and personality traits from `background_details` if present); returns `{"text": "..."}`.
  2. **`POST /player/campaigns/<id>/ai/narration/generate`** — no draft text needed; builds context from: character name/race/class/background, recent narration log (last 5 entries), current scene; instructs Grok to write a short (2–3 sentence) in-character action or dialogue for the player to review; returns `{"text": "..."}`.
  3. **Player campaign page** — add "✨ Clean Up" and "🎲 Generate" buttons below the Post to Story textarea (same visual pattern as DM page). Both use `fetch` to call the routes above and populate the textarea for the player to review before posting.
  4. **Guard**: routes check that the requester has a character in this campaign. AI errors return graceful JSON `{"error": "..."}` and display inline without crashing the form.
  5. **New AI functions** in `services/ai.py`: `cleanup_player_narration(text, character)` and `generate_player_narration(character, recent_log)` — both return `(text, error)` tuple via the existing `_call()` helper.
- **New routes**: two `POST` player AI routes
- **Updated files**: `services/ai.py`, `app.py`, `templates/player/campaign.html`
- **Validation**: Player opens "Post to Story", types a rough sentence → clicks "✨ Clean Up" → textarea is replaced with polished prose. Clicks "🎲 Generate" with empty textarea → a contextual in-character action appears for review. Player edits and posts. Without an API key, a friendly inline error appears instead of a crash.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 41: DM Session Markers & AI Session Summary
- **Source**: DM request (2026-03-21) — DMs want to mark the start of each play session in the narration log and use AI to generate a recap they can share with players.
- **Objectives**: Let the DM insert named session dividers into the narration log, then request an AI-generated summary of everything that happened within a session.
- **Data model**: Session markers are special narration log entries with `type: "session_start"` and a `session_name` field (e.g. "Session 3 — The Haunted Mill"). Regular narration entries have no `type` field (backwards-compatible). Summaries are stored back into the session_start entry as a `summary` field.
- **Tasks**:
  1. **`POST /dm/campaigns/<id>/narration/session/start`** — accepts optional `session_name`; inserts a session marker entry at the end of `narration_log`; auto-numbers if name omitted (`"Session N"`).
  2. **`POST /dm/campaigns/<id>/narration/session/summarize`** — accepts `session_idx` (the index of the session_start entry); collects all narration entries between that marker and the next session marker (or end of log); sends them to xAI Grok with a prompt to write a 3–5 sentence in-world recap; stores the result in `narration_log[session_idx]['summary']`; returns JSON for live update without page reload.
  3. **DM campaign page** — "📅 Start New Session" button in the Narration Log card header creates a new session marker. Session markers render as a styled divider row ("── Session 3 — The Haunted Mill ──") with an "✨ AI Summary" button beside them. Once summarised, the summary displays beneath the divider in italics.
  4. **Player campaign page** — session markers render as read-only dividers with any AI summary shown below them, giving players a clear per-session recap without the DM controls.
  5. **New AI function** `summarize_session(entries, session_name)` in `services/ai.py` — returns `(text, error)` tuple.
- **New routes**: `POST /dm/campaigns/<id>/narration/session/start`, `POST /dm/campaigns/<id>/narration/session/summarize`
- **Updated files**: `services/ai.py`, `app.py`, `templates/dm/campaign.html`, `templates/player/campaign.html`
- **Validation**: DM clicks "Start New Session" → a divider appears at the bottom of both DM and player narration logs. DM runs a session (players post actions, DM narrates). DM clicks "✨ AI Summary" on that session → a 4-sentence recap of the session's events appears below the divider on both views.
- **Status**: Complete ✓ (2026-03-21)

---

### Phase 42: Expansion Content in Rules Reference
- **Source**: User request (2026-03-21) — 9 new expansion docs (files 20-28) added to `Documentation/`; need to surface them in the in-app rules browser.
- **Objectives**: Add all expansion docs to the player and DM rules reference pages with clear source grouping (Core SRD vs. Expansion).
- **Tasks**:
  1. **`app.py`** — add an `EXPANSION_DOCS` list (separate from `PLAYER_DOCS`/`DM_DOCS`) containing tuples for files 20-28, then pass it as a template variable to both `/rules` and `/dm/guide` routes.
  2. **`templates/player/rules.html`** — update the sidebar to render a "Core Rules" section (existing `PLAYER_DOCS`) and an "Expansion Content" section (new `EXPANSION_DOCS`). Use a subtle visual separator (e.g., small header label) between the two groups.
  3. **`templates/dm/guide.html`** — same sidebar grouping treatment; DM sees both `DM_DOCS` and `EXPANSION_DOCS`.
  4. **Route handling** — the existing `_render_doc(filename)` helper already reads any `.md` file from `Documentation/`; no backend change needed beyond adding tuples to the list.
  5. **Source badge** — optionally render a small source tag (XGtE / TCoE / MotM) next to each expansion doc link in the sidebar using the file number as a key.
- **New routes**: None (reuse existing `/rules/<slug>` and `/dm/guide/<slug>` routes)
- **Updated files**: `app.py`, `templates/player/rules.html`, `templates/dm/guide.html`
- **Validation**: Player navigates to Rules → sees "Expansion Content" section in sidebar → clicks "XGtE Subclasses" → full doc renders. DM guide shows the same expansion sidebar.
- **Status**: Complete ✓ (2026-03-22)

---

### Phase 43: Expansion Races in Character Creation
- **Source**: User request (2026-03-21) — `23_MULTIVERSE_RACES.md` contains 31 MotM revised races + Custom Lineage, all using the flexible ASI model (+2/+1 anywhere or +1/+1/+1).
- **Objectives**: Add MotM races to the character creation wizard with full flexible ASI support and a source filter so DMs can enable/disable expansion content per campaign.
- **Tasks**:
  1. **`game_data.py`** — add a `MULTIVERSE_RACES` dict (parallel to `RACES`) with all 31 MotM races + Custom Lineage. Each entry uses `"flex_asi": True` (or a numeric budget) rather than a fixed `asi` dict, reflecting the "put your +2 and +1 anywhere" rule.
  2. **`app.py`** — update character creation route to merge `RACES` and `MULTIVERSE_RACES` into a single options list, tagging each with `source: "PHB"` or `source: "MotM"`. Pass a flag for which sources the campaign allows (default: PHB only; DM can toggle per campaign in `current_state['allowed_sources']`).
  3. **`templates/player/character_create.html`** — update race `<select>` to group options into `<optgroup>` elements ("Core Races" / "Multiverse Races"). When a MotM race is selected, show flexible ASI inputs instead of the fixed ASI display.
  4. **`templates/dm/campaign.html`** — add a Campaign Settings card (or expand existing settings) with checkboxes to allow PHB-only, XGtE, TCoE, MotM races. Stored in `campaign.current_state['allowed_sources']`.
  5. **AI character generator** — update prompt in `services/ai.py` to list MotM races when allowed, noting they use the flexible ASI rule.
- **New routes**: `POST /dm/campaigns/<id>/settings/sources` (or fold into existing campaign settings route)
- **Updated files**: `game_data.py`, `app.py`, `services/ai.py`, `templates/player/character_create.html`, `templates/dm/campaign.html`
- **Validation**: DM enables MotM races. Player creates a character, selects "Astral Elf" from Multiverse Races group, sees flexible ASI inputs, distributes +2 and +1 freely. PHB race creation is unchanged.
- **Status**: Pending

---

### Phase 44: Subclass Tracking & Expansion Subclasses
- **Source**: User request (2026-03-21) — files 20 (XGtE) and 21 (TCoE) contain 55 combined subclasses not yet tracked in character data.
- **Objectives**: Store a character's subclass in character data and surface XGtE/TCoE subclasses in character creation and the AI character generator.
- **Tasks**:
  1. **`game_data.py`** — add a `SUBCLASSES` dict keyed by class name, each value a list of `{"name": str, "source": str, "description": str}` entries covering all PHB, XGtE, and TCoE subclasses. PHB subclasses are already implied by the classes reference; expand from files 20 and 21.
  2. **`models.py` / character data** — subclass is stored in `character.spells['subclass']` (already exists as a field in some characters). No schema migration needed; use `flag_modified` pattern after writes.
  3. **`templates/player/character_create.html`** — after the class `<select>`, add a subclass `<select>` populated via JS from `SUBCLASSES[selected_class]`. Subclasses from expansion sources show a source badge. "Choose at Level 3" note for classes that pick subclass at level 3.
  4. **`templates/player/character_sheet.html`** (or equivalent) — display selected subclass name and source prominently on the character sheet.
  5. **AI DM / AI character generator** — inject the character's subclass name and its key features into AI prompts (from `game_data.SUBCLASSES`) so the AI can reference subclass abilities during play.
- **New routes**: None (subclass stored with existing character update routes)
- **Updated files**: `game_data.py`, `app.py`, `services/ai_dm.py`, `templates/player/character_create.html`
- **Validation**: Player creates a Fighter, selects "Echo Knight" (TCoE) as subclass. Character sheet shows "Echo Knight (Fighter — TCoE)". AI DM narrates combat referencing Manifest Echo ability.
- **Status**: Pending

---

### Phase 45: Expansion Spells & Feats in Character Data
- **Source**: User request (2026-03-21) — `24_EXPANSION_SPELLS.md` (cantrips through 9th level) and `25_EXPANSION_FEATS.md` (TCoE general feats + XGtE racial feats) not yet available in the app.
- **Objectives**: Make expansion spells searchable in spell reference and add feat tracking to character sheets.
- **Tasks**:
  1. **`game_data.py`** — add `EXPANSION_SPELLS` list (name, level, school, classes, source) mirroring structure of any existing spell list. Add `FEATS` dict (feat name → description, prerequisites, source).
  2. **`templates/player/rules.html`** (spell reference view) — merge `EXPANSION_SPELLS` into the spell list display when viewing `24_EXPANSION_SPELLS.md`, or add a separate "Expansion Spells" tab on the spellcasting reference page.
  3. **Character sheet / spells** — when a player prepares or knows expansion spells, the AI DM's prompt should include the spell's description from `EXPANSION_SPELLS` so it can adjudicate correctly.
  4. **Feat tracking** — add a `feats` list to `character.spells` (same JSON column). Character creation and a future character editor route allow adding feats from `FEATS`. Display on character sheet.
  5. **AI context** — `services/ai_dm.py` inject any feats the character has into the AI prompt with their mechanical effects so the AI can apply them during skill checks and combat.
- **New routes**: None critical; optionally `POST /player/characters/<id>/feats` for feat management
- **Updated files**: `game_data.py`, `services/ai_dm.py`, `templates/player/character_sheet.html`
- **Validation**: Character with "Fey Touched" feat — AI applies Misty Step and +1 to one mental stat automatically. Expansion spell "Shadow Blade" shows in spell reference with school and classes listed.
- **Status**: Pending

---

### Phase 46: DM Group Patrons & Campaign Downtime
- **Source**: User request (2026-03-21) — `28_EXPANSION_DM_TOOLS.md` contains group patron rules (guilds, military, etc.) and downtime activity system.
- **Objectives**: Let the DM assign a group patron to the campaign and track player downtime activities between sessions.
- **Tasks**:
  1. **`game_data.py`** — add `GROUP_PATRONS` dict (patron type → perks, contact NPC template, sample quests) and `DOWNTIME_ACTIVITIES` dict (activity → description, check, outcome) from the expansion DM tools doc.
  2. **Campaign settings** — store `patron_type` and `downtime_log` (list of `{character, activity, result, session}`) in `campaign.current_state`. Add DM route `POST /dm/campaigns/<id>/patron` to set/change patron type.
  3. **`templates/dm/campaign.html`** — add a "Group Patron" card in the DM panel: patron name, perks summary, and a button to generate AI quest hooks tailored to that patron. Add a "Downtime" card listing each character's declared downtime activity for the current between-session period.
  4. **AI quest hook generator** — new route `POST /dm/campaigns/<id>/patron/quest` calls xAI Grok with patron type, party composition, and recent narration log to generate 2-3 thematic quest hooks in JSON. Rendered on the DM page.
  5. **Player downtime** — optional: allow players to submit their downtime activity via the player page; DM sees submissions in the Downtime card.
- **New routes**: `POST /dm/campaigns/<id>/patron`, `POST /dm/campaigns/<id>/patron/quest`, optionally `POST /player/campaigns/<id>/downtime`
- **Updated files**: `game_data.py`, `app.py`, `services/ai.py`, `templates/dm/campaign.html`, optionally `templates/player/campaign.html`
- **Validation**: DM sets patron to "Thieves' Guild". DM page shows patron card with guild perks. DM clicks "Generate Quest Hooks" → 3 guild-flavored hooks appear. Players submit downtime activities; DM sees "Aria — Carousing", "Theron — Training".
- **Status**: Pending

---

### Phase 47: AI Context Enrichment with Expansion Content
- **Source**: User request (2026-03-21) — the AI DM currently works from PHB rules only; expansion subclasses, spells, feats, and patron perks should inform its narration and rulings.
- **Objectives**: Dynamically inject relevant expansion reference text into AI prompts based on what content each character actually uses, without bloating every prompt with all 9 expansion files.
- **Tasks**:
  1. **Context selector** (`services/ai_dm.py`) — before building AI prompts, inspect each character's data: if they have an XGtE/TCoE subclass, pull that subclass's feature blurb from `game_data.SUBCLASSES`; if they have expansion spells prepared, pull those spell descriptions from `game_data.EXPANSION_SPELLS`; if they have feats, pull feat mechanics from `game_data.FEATS`.
  2. **Patron context** — if the campaign has a patron type set, inject a short patron description and its quest-hook flavor into scene-building and NPC-generation prompts.
  3. **MotM race traits** — if a character is a MotM race, inject that race's traits (from `game_data.MULTIVERSE_RACES`) into combat and skill-check prompts so the AI knows about abilities like Astral Elf's Astral Fire cantrip swap.
  4. **Token budget guard** — cap injected expansion content at ~400 tokens per prompt to avoid context bloat. Prioritize: (a) active character's subclass features, (b) spells being cast, (c) feats relevant to the action type, (d) patron flavor.
  5. **`17_LLM_INSTRUCTIONS.md` reference** — optionally update this doc to note that expansion content is injected selectively, not wholesale, so future LLM integrations can follow the same pattern.
- **New routes**: None (internal prompt-building change)
- **Updated files**: `services/ai_dm.py`, `services/ai.py`, `Documentation/17_LLM_INSTRUCTIONS.md`
- **Validation**: Fighter with Echo Knight subclass takes an attack action → AI narration mentions the Manifest Echo. Warlock casts Shadow Blade (TCoE) → AI describes the psychic blade correctly. Token count of AI requests stays under the model's practical limit.
- **Status**: Pending

---

## Wishlist (Future Consideration)
*Not prioritized for active development; revisit after Phase 13.*

- **AI Rules Q&A (RAG over Documentation)**: Index the `Documentation/*.md` files so players and the DM can ask natural-language questions (e.g. "Can I bonus action after an Attack action?") and get answers grounded in the actual rule text via xAI Grok. Would require a vector store or simple BM25 retrieval layer feeding relevant chunks into the Grok context.
- **D&D Beyond Import**: Allow players to paste a D&D Beyond character URL or upload a PDF export to auto-fill the character creation form. Viability depends on D&D Beyond's API/export format — treat as exploratory research first.
- **Custom Rules & Homebrew Classes**: Let the DM define custom classes, races, and mechanics per campaign (stored in `current_state` or a separate `campaign_rules` JSON field). The character creation wizard would merge official and homebrew options for that campaign. Complex feature — design a data schema before implementing.
- **Battle Board Integration**: Add an optional field on the campaign for an external battle board URL (e.g., Owlbear Rodeo). If set, show a "Open Battle Board" button/link that opens it in a new tab for all players.
- **Preloaded Campaigns**: Bundle a full "Lost Mines of Phandelver" (or other OGL-compatible) campaign as an importable `.md` bundle using the Phase 8 format.

---

## Risks and Mitigations
- **Complexity of Rules**: Start with simplified versions (e.g., basic combat); reference documentation for accuracy.
- **Real-Time Updates**: Use polling initially; upgrade to WebSockets if lag becomes an issue.
- **Multi-User Sync**: Store all state on server; use locks for critical sections (e.g., during turns).
- **Scalability**: SQLite is fine for small groups; monitor for performance.

## Timeline and Resources
- **Total Estimate**: 10-15 days for MVP, assuming 4-6 hours/day.
- **Tools Needed**: VS Code for development; browser for testing; Git for version control.
- **Dependencies**: Flask, SQLAlchemy, basic HTML/JS (no heavy frameworks).