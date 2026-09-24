import sqlite3
from pathlib import Path
from collector import config

class StorageHandler:
    def __init__(self):
        config._DATA_DIR.mkdir(exist_ok=True)
        self.db = sqlite3.connect(config._DB_PATH)
        self.create_table()

    def create_table(self):
        sql = config._SCHEMA_PATH.read_text(encoding="utf-8")
        self.db.executescript(sql)
        self.db.commit()

    def write_hr_reading_to_db(self, session_id: str, timestamp: str, bpm: int):
        self.db.execute(
            "INSERT INTO hr_readings (session_id, timestamp, bpm) VALUES (?, ?, ?)",
            (session_id, timestamp, bpm),
        )
        self.db.commit()
