# HR Monitor

Prototype for reading heart-rate data from a Garmin Forerunner 55 over Bluetooth Low Energy (BLE), persisting readings to SQLite, and plotting queried windows.

## Current status

The app offers a simple CLI menu:

1. **Record new HR data** — scan → connect → subscribe to HR Measurement notifications, print BPM, and save each reading under a session
2. **Query existing HR data** — load rows in a time window from SQLite and open a Plotly line chart

| Path | Role |
| --- | --- |
| `main.py` | Entry point: record loop or query + chart |
| `collector/scanner.py` | BLE discovery via [Bleak](https://github.com/hbldh/bleak); returns the Forerunner 55 when found |
| `collector/connection.py` | Wraps `BleakClient`; connects to the scanned device |
| `collector/hr_listener.py` | Subscribes with `start_notify`, parses HR Measurement bytes into BPM |
| `collector/session.py` | Groups one connect/subscribe run under a UUID `session_id`; writes start/end markers and readings |
| `collector/storage_handler.py` | Inserts rows into SQLite at `data/HR_data.db` |
| `collector/config.py` | Paths for data dir, DB, and schema |
| `db/schema.sql` | SQLite table definition for `hr_readings` |
| `scripts/query_handler.py` | Time-range `SELECT` against `hr_readings` |

### Recording flow

Heart rate is delivered as **GATT notifications**, not a one-shot read:

1. Enable HR broadcast on the watch, then wait for the connect countdown
2. `start_notify` on characteristic `00002a37-…` and start a session (`session_id` UUID)
3. Each notification is parsed to BPM, printed, and stored with timestamp `dd-Mon-yy HH:MM:SS.mmm`
4. On stop (`Ctrl+C`), the listener unsubscribes, writes a session end marker (`bpm` NULL), and disconnects

Session start/end rows use the same `session_id` with `bpm` NULL; actual readings have integer BPM.

### Query flow

Enter start and end times matching stored timestamps, e.g. `22-Sep-26 14:53:21.029` (seconds optional depending on your filter strings). Matching rows are plotted with Plotly Express.

## Roadmap

Phases (persist → SQL windows → API → graphs → Docker/CI → hosting): **[ROADMAP.md](ROADMAP.md)**.

## Project structure

Repo root keeps `README.md`, `ROADMAP.md`, `.gitignore`, and `main.py`.  
**Backend:** `collector/` (BLE ingest + sessions), `db/` (schema / later SQLAlchemy), `api/` (FastAPI).  
**Frontend:** `web/` (charts by date).  
**Other:** `data/` (local SQLite, gitignored), `tests/`, `scripts/`.  
No `src/` for now — optional later if we package the app.

```text
HR_monitor/
├── .gitignore
├── README.md
├── ROADMAP.md
├── main.py
├── data/
├── collector/
│   ├── config.py
│   ├── scanner.py
│   ├── connection.py
│   ├── hr_listener.py
│   ├── session.py
│   └── storage_handler.py
├── db/
│   └── schema.sql
├── api/
│   └── routes/
├── web/
│   └── static/
├── tests/
└── scripts/
    └── query_handler.py
```

## Direction

Later, this is meant to become a **full-stack app** that shows **live** heart-rate (and related) data on screen.

Live updates will only be as good as the hardware and firmware allow:

- **TP-Link Bluetooth 5.4 USB adapter** — radio range, Windows BLE stack, and how quickly advertisements and GATT notifications arrive
- **Garmin Forerunner 55** — which BLE services it exposes, and whether heart-rate streams reliably to third-party clients (Garmin watches often limit this compared with a dedicated chest strap)

If the watch does not stream HR over BLE, the UI can still be built, but the live feed will be limited to whatever the device exposes.

## Hardware

| Role | Device |
| --- | --- |
| BLE adapter | TP-Link Bluetooth 5.4 USB adapter |
| Watch | Garmin Forerunner 55 |

## Run

```powershell
python -m pip install bleak plotly
python main.py
```

Keep the USB adapter plugged in and Bluetooth enabled. For recording, enable HR broadcast on the watch and wear it (or otherwise keep HR sensing active). The app waits 10 seconds before scanning; after connect it prints readings until you stop with `Ctrl+C`. For querying, use timestamps in the same format as stored rows (e.g. `22-Sep-26 14:53:21.029`).
