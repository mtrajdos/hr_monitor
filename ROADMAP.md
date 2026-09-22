# Roadmap

Step-by-step plan from the **working BLE prototype** to a full-stack app.  
Each phase ends with testable vertical slices.

---

## Mental model (rationale for refreshing on SQL)

Each notify becomes one row:

| recorded_at (timestamp) | bpm |
| ----------------------- | --- |
| 2026-09-22 12:44:03     | 72  |
| 2026-09-22 12:44:04     | 73  |
| …                       | …   |

A **recording window** (e.g. 12:44–12:48 on 22/09/2026) will be displayed through SQL queries, e.g. :

```sql
SELECT recorded_at, bpm
FROM hr_readings
WHERE recorded_at >= '2026-09-22 12:44:00'
  AND recorded_at <  '2026-09-22 12:48:00'
ORDER BY recorded_at;
```

Optionally group rows into **sessions** (one BLE connect run = one window). Same idea, cleaner browsing.

---

## Done

- [x] Scan for Forerunner 55  
- [x] Connect with Bleak  
- [x] Subscribe to HR Measurement notifications  
- [x] Parse bytes → BPM and print in a loop  

**Current files:** `main.py`, `scanner.py`, `connection.py`, `hr_listener.py`

---

## Phase 1 — Persist timestamped readings (local, minimal)

**Goal:** Stop losing data when the terminal closes. Every BPM is saved with a timestamp.

**Deliverables**

1. Choose first storage: **SQLite file** (zero install) → later migrate same schema to PostgreSQL.  
2. Implement `storage_handler.py`: `save_reading(recorded_at, bpm)`.  
3. On each notify in `hr_listener` / `main`, call save.  
4. Table roughly: `hr_readings(id, recorded_at, bpm)`.  
5. Functional SQL query: “print all readings between two local times.”  

**Done when:** You run a session, quit, reopen DB, and still see that day’s points for a graph.

**Docs:** Short “How data is stored” section in README.

**New pieces only:** `storage_handler.py`, `hr_monitor.db` (gitignored), `scripts/query_window.py`.

---

## Phase 2 — Sessions / time windows

**Goal:** Browse “recordings” as windows, not only raw points.

**Deliverables**

1. Table `sessions(id, started_at, ended_at, note)`.  
2. Start a session when BLE connects; end on disconnect / Ctrl+C.  
3. Each reading links to `session_id`.  
4. Query: list sessions for a date; load all points for one session (graph-ready).  

**Done when:** You can answer: “On 22/09/2026 between 12:44 and 12:48, these were the BPM values” via a query or small CLI.

**Docs:** Describe session vs reading in README.

---

## Phase 3 — Real SQL database (PostgreSQL) + SQLAlchemy

**Goal:** Same behaviour, job-market stack (PostgreSQL, SQLAlchemy, migrations).

**Deliverables**

1. Docker Compose service: `postgres` only.  
2. SQLAlchemy models + Alembic migration matching Phase 1–2 schema.  
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
   - `GET /api/sessions?date=2026-09-22`  
   - `GET /api/readings?from=...&to=...` or `?session_id=...`  
2. Run locally: `uvicorn` + open `/docs` (Swagger).  
3. A few **pytest** tests for parse + one endpoint.  

**Done when:** Browser or `curl` gets graph-ready JSON for a window.

**New pieces:** `api/` (small), `tests/`.

---

## Phase 5 — Simple website: browse by date + continuous graph

**Goal:** Click a date (or session) → see a continuous HR chart.

**Deliverables**

1. One HTML page (Chart.js or Plotly) calling the API.  
2. Date list + chart for selected window.  
3. Still local: API + static files on your machine.  

**Done when:** You can demo a recording visually without explaining SQL.

**New pieces:** `web/` (keep thin).

---

## Phase 6 — Packaging & QA

**Goal:** Looks like something a team could clone and run.

**Deliverables**

1. `Dockerfile` for API; Compose: `postgres` + `api`.  
2. GitHub Actions: install deps → pytest on push.  
3. README: architecture diagram (text), how to run collector vs API.  
4. `.env.example`, clear gitignore (no secrets, no huge DB dumps).  

**Done when:** Fresh clone + Compose instructions work for the API/DB part (collector may stay “on your PC with the USB dongle”).
