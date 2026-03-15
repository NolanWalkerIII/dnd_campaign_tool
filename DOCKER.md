# Docker Reference — D&D Campaign Manager

## Setup

### 1. Configure environment variables
Copy the example env file and add your xAI API key:
```bash
cp .env.example .env
# Edit .env and replace 'your_xai_api_key_here' with your real key
```
The `.env` file is gitignored and will never be committed.

### 2. Build and launch
```bash
docker compose up --build -d
```
The app will be available at **http://localhost:5001**.

---

## Common Commands

| Task | Command |
|------|---------|
| Build and start (detached) | `docker compose up --build -d` |
| Start existing image | `docker compose up -d` |
| Stop container | `docker compose down` |
| View live logs | `docker logs -f dndidea-dnd-1` |
| Check container status | `docker ps` |

---

## Picking Up Config Changes

### After editing `.env`
`docker compose restart` does **not** re-read `env_file` — it only restarts the process. You must recreate the container:
```bash
docker compose up -d
```
This picks up any changes to `.env` or `docker-compose.yml` without a full rebuild.

### After editing Python/template files
A rebuild is required to copy the updated files into the image:
```bash
docker compose down
docker compose build
docker compose up -d
```

### After editing `requirements.txt`
Force a clean pip install with `--no-cache`:
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `XAI_API_KEY` | No | xAI Grok API key — enables the ✨ Clean Up and 🎲 Generate AI buttons on the DM campaign page. Without it, buttons show a graceful "not set" message. |
| `FLASK_ENV` | Set by compose | Set to `production` in `docker-compose.yml`. |

---

## Data Persistence

The SQLite database is stored in `./instance/dnd.db` on the host and mounted into the container:
```yaml
volumes:
  - ./instance:/app/instance
```
This means your data survives container rebuilds and restarts. To reset the database, delete `instance/dnd.db`.

---

## Ports

| Host | Container | Service |
|------|-----------|---------|
| 5001 | 5000 | Flask app |

To change the host port, edit the `ports` entry in `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:5000"
```

---

## Troubleshooting

**Internal Server Error on first launch**
The app runs a startup migration to add any missing database columns. If you see a 500 on the very first request, restart the container — the migration runs at startup and should self-heal:
```bash
docker compose restart
```

**AI buttons show "XAI_API_KEY is not set"**
1. Ensure `.env` exists and contains `XAI_API_KEY=your_real_key`
2. Recreate the container (restart alone is not enough):
   ```bash
   docker compose up -d
   ```
3. Verify the key is loaded inside the container:
   ```bash
   docker exec dndidea-dnd-1 sh -c 'echo "KEY_SET=${XAI_API_KEY:+yes}"'
   ```

**Port 5001 already in use**
```bash
# Find what's using it
lsof -i :5001
# Or change the port in docker-compose.yml
```
