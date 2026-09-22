import sqlite3
from pathlib import Path

class StorageHandler:
    def __init__(self):
        self.db = sqlite3.connect('MT_data.db')
        self.create_table()

    def create_table(self):
        sql = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        self.db.executescript(sql)
        self.db.commit()

    def get_rows_by_timestamp(self, timestamp: str):
        return self.db.execute("SELECT * FROM hr_readings WHERE timestamp = ?", (timestamp,))
    
    def set_row(self, timestamp: str, bpm: int):
        self.db.execute(
            "INSERT INTO hr_readings (timestamp, bpm) VALUES (?, ?)",
            (timestamp, bpm),
        )
        self.db.commit()

    