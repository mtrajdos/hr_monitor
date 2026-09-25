"""Generate synthetic HR sessions shaped like data/HR_data.db."""
import random
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SRC_DB = _ROOT / "data" / "HR_data.db"
_DEST_DB = _ROOT / "data" / "synthetic_HR_data.db"
_SCHEMA_SQL = (_ROOT / "db" / "schema.sql").read_text(encoding="utf-8")

# Real notify spacing is ~0.5–1.2 s; ~1 s => ~10 min ≈ 600 rows
_SECONDS_PER_READING = 1.0
_SESSION_MINUTES_LO = 8.0
_SESSION_MINUTES_HI = 12.0
_N_SESSIONS = 40
_TS_FMT = "%d-%b-%y %H:%M:%S.%f"


def _format_timestamp(dt: datetime) -> str:
    return dt.strftime(_TS_FMT)[:-3]


def main() -> None:
    src = sqlite3.connect(_SRC_DB)
    bpm_min, bpm_max, bpm_mean = src.execute(
        "SELECT MIN(bpm), MAX(bpm), AVG(bpm) FROM hr_readings"
    ).fetchone()
    src.close()
    bpm_min, bpm_max = int(bpm_min), int(bpm_max)
    bpm_mean = float(bpm_mean)

    # 2. Create destination DB using the existing schema.sql
    _DEST_DB.parent.mkdir(exist_ok=True)
    if _DEST_DB.exists():
        _DEST_DB.unlink()
    dest = sqlite3.connect(_DEST_DB)
    dest.executescript(_SCHEMA_SQL)

    base = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    total_rows = 0

    for s in range(_N_SESSIONS):
        session_id = str(uuid.uuid4())

        duration_min = random.uniform(_SESSION_MINUTES_LO, _SESSION_MINUTES_HI)
        n_rows = max(1, int(duration_min * 60 / _SECONDS_PER_READING))

        t = base + timedelta(days=s // 8, hours=(s % 8) * 2, minutes=random.randint(0, 30))
        bpm = int(round(random.gauss(bpm_mean, (bpm_max - bpm_min) / 6)))
        bpm = max(bpm_min, min(bpm_max, bpm))

        rows: list[tuple[str, str, int]] = []
        for _ in range(n_rows):
            rows.append((session_id, _format_timestamp(t), bpm))
            t += timedelta(seconds=_SECONDS_PER_READING)
            bpm += random.choice((-2, -1, -1, 0, 0, 0, 1, 1, 2))
            bpm = max(bpm_min, min(bpm_max, bpm))

        # d) End session: persist this session's rows
        dest.executemany(
            "INSERT INTO hr_readings (session_id, timestamp, bpm) VALUES (?, ?, ?)",
            rows,
        )
        dest.commit()
        total_rows += n_rows
        print(f"Session {s + 1}/{_N_SESSIONS}: {n_rows} rows ({duration_min:.1f} min)")

    dest.close()
    print(f"Done: {total_rows} rows -> {_DEST_DB}")


if __name__ == "__main__":
    main()
