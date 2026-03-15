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

### Phase 14: Campaign Progress Tracker & Story Forks
- **Objectives**: Let the DM track where the party is in a structured campaign and model story branches/forks.
- **Tasks**:
  1. **Campaign Progress / Chapter Tracker**: Add a `chapters` list to `current_state`. Each chapter has a title, a description/summary, a status (`upcoming` / `active` / `completed`), and optional notes. DM can add, reorder, mark complete, and add notes to chapters from the campaign page.
  2. **Progress Panel**: Show a visual chapter timeline on the DM campaign page (and a read-only version for players) so everyone can see where they are in the story. The active chapter is highlighted; completed ones are checked off.
  3. **Story Forks**: Each chapter can have `branches` — named alternate paths (e.g. "Players follow the merchant" vs "Players investigate the cave"). The DM can create branches, pick the one the party took, and add notes per branch. Unchosen branches are greyed out but preserved so the DM can reference or reuse them.
  4. **AI-Assisted Chapter Summary**: An optional "Summarise this chapter" button (using xAI Grok) that reads the narration log entries since the chapter started and generates a short summary to pre-fill the chapter notes field.
- **Deliverables**: Chapter data model in `current_state`; DM chapter management UI; player progress view; story fork UI; AI chapter summary button.
- **Validation**: DM can create a 3-chapter adventure with a fork at chapter 2; marking chapter 1 complete updates the timeline; choosing a fork greys out the alternate branch.
- **Status**: Not started

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