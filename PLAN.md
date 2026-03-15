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

## Wishlist (Future Consideration)
*Not prioritized for active development; revisit after Phase 10.*

- **Battle Board Integration**: Add an optional field on the campaign for an external battle board URL (e.g., Owlbear Rodeo). If set, show a "Open Battle Board" button/link that opens it in a new tab for all players. Simple to implement — just a URL field and a link render.
- **Preloaded Campaigns**: Bundle a full "Lost Mines of Phandelver" (or other OGL-compatible) campaign as an importable `.md` bundle (using the Phase 8 format). Includes all named NPCs, location descriptions, and encounter templates. DMs can load it as a starting point and customize from there.

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