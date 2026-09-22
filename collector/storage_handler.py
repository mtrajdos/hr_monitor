import sqlite3
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _ROOT / "data"
_DB_PATH = _DATA_DIR / "MT_data.db"
_SCHEMA_PATH = _ROOT / "db" / "schema.sql"


class StorageHandler:
    def __init__(self):
        _DATA_DIR.mkdir(exist_ok=True)
        self.db = sqlite3.connect(_DB_PATH)
        self.create_table()

    def create_table(self):
        sql = _SCHEMA_PATH.read_text(encoding="utf-8")
        self.db.executescript(sql)
        self.db.commit()

    def get_rows_by_timestamp(self, timestamp: str):
        return self.db.execute(
            "SELECT * FROM hr_readings WHERE timestamp = ?",
            (timestamp,),
        )

    def set_row(self, timestamp: str, bpm: int):
        self.db.execute(
            "INSERT INTO hr_readings (timestamp, bpm) VALUES (?, ?)",
            (timestamp, bpm),
        )
        self.db.commit()
