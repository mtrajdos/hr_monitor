import sqlite3
from pathlib import Path
from collector import config

class QueryHandler:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or (config._ROOT / "data" / "HR_data.db")
        self.db = sqlite3.connect(self.db_path)

    def get_rows_between_times(self, start_time: str, end_time: str):
        return self.db.execute("SELECT * FROM hr_readings WHERE timestamp BETWEEN ? AND ?", (start_time, end_time)).fetchall()