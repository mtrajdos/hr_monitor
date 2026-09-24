# Roadmap

Step-by-step plan from the **working BLE prototype** to a full-stack app.  
Each phase ends with testable vertical slices.

---

## Mental model (rationale for refreshing on SQL)

Each notify becomes one row:

| session_id | timestamp (receive time) | bpm |
| ---------- | ------------------------ | --- |
| `a1b2-…`   | 22-Sep-26 13:42:46       | 74  |
| `a1b2-…`   | 22-Sep-26 13:42:47       | 74  |
| …          | …                        | …   |

A **recording window** (e.g. 12:44–12:48 on 22/09/2026) is displayed through SQL, e.g.:

```sql
SELECT timestamp, bpm
FROM hr_readings
WHERE timestamp >= '...' AND timestamp < '...'
ORDER BY timestamp;
```

One BLE connect run shares one UUID `session_id`. No separate `sessions` table: group or filter by that column (`MIN`/`MAX(timestamp)` per id, or `WHERE session_id = …`).

(Column is currently named `timestamp`; prefer ISO/`recorded_at` later if we tighten the schema.)

---

## Done

### Phase 0 — BLE collector

- [x] Scan for Forerunner 55  
- [x] Connect with Bleak  
- [x] Subscribe to HR Measurement notifications (`start_notify` once)  
- [x] Parse bytes → BPM and print in a loop  
- [x] Clean shutdown (`stop_notify` + disconnect on Ctrl+C)  

### Phase 1 — Persist timestamped readings

- [x] SQLite storage (`data/HR_data.db`, gitignored)  
- [x] `collector/storage_handler.py` — insert + commit  
- [x] Save on each reading from `hr_listener`  
- [x] Schema `db/schema.sql` — `hr_readings(sample_id, session_id, timestamp, bpm)`  
- [x] Data survives process exit (reopen DB → rows still there)  
- [x] CLI/script: readings between two local times (`scripts/query_handler.py`) + Plotly chart  

### Phase 2 — Sessions / time windows

**Design:** `session_id` on each reading is enough. No separate `sessions` table unless we later need notes/status without aggregating readings.

- [x] UUID `session_id` per recording run (`collector/session.py`)  
- [x] Each reading stores `session_id`  
- [x] Time-window query answers “BPM between 12:44 and 12:48” via CLI  
- [x] README: session vs reading (id-on-row model, no marker rows)  

Optional later (not blocking Phase 3): CLI to list distinct `session_id`s for a date / load by id.

### Scaffolding

- [x] Target folders: `collector/`, `db/`, `api/`, `web/`, `tests/`, `scripts/`, `data/`  
- [x] Modules in `collector/`; schema in `db/`  
- [x] `.gitignore` for `__pycache__/`, `*.db`, wal/shm sidecars  
- [x] README project structure + link to this roadmap  

**Layout now:**

```text
main.py
collector/   scanner, connection, hr_listener, session, storage_handler
db/          schema.sql
data/        HR_data.db (local only)
api/, web/, tests/, scripts/
```

---

## Next up

**Phase 3 — PostgreSQL + SQLAlchemy** (same `hr_readings` + `session_id` schema).

---

## Phase 3 — Real SQL database (PostgreSQL) + SQLAlchemy

**Goal:** Same behaviour, job-market stack (PostgreSQL, SQLAlchemy, migrations).

**Deliverables**

1. Docker Compose service: `postgres` only.  
2. SQLAlchemy models + Alembic migration matching Phase 1–2 schema (`hr_readings` with `session_id`).  
3. Point `storage_handler` at Postgres (env var for connection string).  
4. Keep SQLite as optional/dev fallback if useful.  

**Done when:** Compose up → collector writes to Postgres → `psql` or a script returns a time window.

**New pieces:** `docker-compose.yml`, `db/models.py`, `db/migrations/`, `.env.example`.

---

## Phase 4 — Read API (no fancy UI yet)

**Goal:** HTTP endpoints that return JSON usable by any chart library.

**Deliverables**

1. FastAPI app with:  
   - `GET /api/days` — dates that have data  
   - `GET /api/sessions?date=2026-09-22` — distinct `session_id`s (and min/max time) for that date  
   - `GET /api/readings?from=...&to=...` or `?session_id=...`  
2. Run locally: `uvicorn` + open `/docs` (Swagger).  
3. A few **pytest** tests for parse + one endpoint.  

**Done when:** Browser or `curl` gets graph-ready JSON for a window.

**New pieces:** fill `api/`, `tests/`.

---

## Phase 5 — Simple website: browse by date + continuous graph

**Goal:** Click a date (or session) → see a continuous HR chart.

**Deliverables**

1. One HTML page (Chart.js or Plotly) calling the API.  
2. Date list + chart for selected window.  
3. Still local: API + static files on your machine.  

**Done when:** You can demo a recording visually without explaining SQL.

**New pieces:** fill `web/`.

---

## Phase 6 — Packaging & QA

**Goal:** Looks like something a team could clone and run.

**Deliverables**

1. `Dockerfile` for API; Compose: `postgres` + `api`.  
2. GitHub Actions: install deps → pytest on push.  
3. README: how to run collector vs API.  
4. `.env.example`, keep gitignore tight (no secrets, no DB dumps).  

**Done when:** Fresh clone + Compose instructions work for the API/DB part (collector may stay “on your PC with the USB dongle”).

---

## Phase 7 — Public demo (cheap hosting)

Deploy API + DB (and/or sample data); collector stays on the PC with the watch. See earlier plan notes in chat / README Direction.
