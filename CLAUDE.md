# CLAUDE.md — D&D Campaign Tool (Quester Ledger)

## Project Overview

Web-based D&D 5e campaign manager with Discord bot, SMS play mode (Twilio), and REST API for AI agent gameplay. Built by John for Nolan (repo owner).

- **Repo**: `NolanWalkerIII/dnd_campaign_tool`
- **Production**: `questerledger.johnbest.ai` (server: `claude@port.jsbjr.digital`)
- **Active branch**: `feature/claude-api`

## Quick Start (Local)

```bash
source venv/bin/activate
PORT=5050 python app.py
```

Port 5050 because macOS AirPlay blocks 5000.

## Quick Start (Docker — Nolan's Mac Mini)

```bash
git checkout feature/claude-api
cp .env.example .env    # fill in API keys
docker compose up --build -d
# App at http://localhost:5001
```

## Production Deploy

Production has **no git** — deploy by copying files:

```bash
scp <changed_files> claude@port.jsbjr.digital:/home/claude/questerledger/
ssh claude@port.jsbjr.digital "cd /home/claude/questerledger && docker-compose down && docker-compose build && docker-compose up -d"
```

**Important**: Production uses `docker-compose` (hyphenated, v2.20.3), NOT `docker compose`.

## Environment Variables

Required in `.env` (never commit this file):

| Variable | Description |
|----------|-------------|
| `XAI_API_KEY` | xAI Grok API (use free-tier key starting with `xai-qe3k...`) |
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `DISCORD_CLIENT_ID` | Discord application ID: `1482816007872577696` |
| `CLAUDE_API_KEY` | Bearer token for REST API auth |

Optional: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`

## Key Architecture

| File | Purpose |
|------|---------|
| `app.py` | Flask app factory, route registration, DB migration |
| `models.py` | SQLAlchemy models: User, Character, Campaign, DiceRoller |
| `api_routes.py` | REST API (20+ endpoints, Bearer token auth) |
| `sms_routes.py` | Twilio SMS webhook |
| `services/discord_bot.py` | Discord bot: slash commands, channel management |
| `services/ai_dm.py` | AI DM agent (intent → mechanics → narration) |
| `services/engine.py` | Pure-function game logic (rolls, attacks, skill checks) |
| `services/ai.py` | xAI Grok API wrapper |
| `game_data.py` | D&D 5e static data (races, classes, skills, spells) |

## Critical Gotchas

1. **One Discord bot at a time** — same token, only one instance. Kill local before production.
2. **JSON columns** — use `from sqlalchemy.orm.attributes import flag_modified; flag_modified(obj, 'column_name')` after mutating any JSON column. NOT `db.session.flag_modified()`.
3. **Discord defer()** — always `interaction.response.defer()` before long operations. Wrap deferred flows in try/except so `interaction.followup.send()` always fires.
4. **docker-compose.yml** — production needs simple string `env_file: - .env` format (v2.20.3 doesn't support `path:` / `required:` syntax).

## Testing

```bash
python -m pytest tests/test_suite.py -v    # 38 tests
```

Discord and SMS features are tested manually. See the vault at `ObsidianVault/Projects/Code/DnDCampaignTool/` for full testing procedures and handoff notes.

## Discord Channels (created by /setup)

| Channel | Visibility | Purpose |
|---------|-----------|---------|
| quest-board | Read-only | Story updates, quest hooks |
| tavern | Open | Main gameplay |
| combat | Open | Combat encounters |
| dice-log | Read-only | Roll log |
| character-sheets | Read-only | Character stats |
| dm-screen | DM-only (hidden) | DM commands |
| debug | DM-only (hidden) | Bot diagnostics |

## Discord Slash Commands

**DM commands**: `/setup`, `/start`, `/reset`, `/scene`, `/combat`, `/npc`, `/damage`, `/heal`, `/whisper`, `/recap`, `/agent`

**Player commands**: `/join`, `/verify`, `/action`, `/roll`, `/attack`, `/check`, `/stats`

## API Endpoints for AI Agents

```bash
# Get game context
curl -H "Authorization: Bearer $CLAUDE_API_KEY" \
  "http://localhost:5050/api/play/context?campaign_id=1&character_id=1"

# Submit an action as a character
curl -X POST -H "Authorization: Bearer $CLAUDE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"campaign_id": 1, "character_id": 1, "message": "I search the room"}' \
  "http://localhost:5050/api/play"
```
