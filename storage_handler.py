import sqlite3

class StorageHandler:
    def __init__(self):
        self.timestamps = tuple()
        self.db = sqlite3.connect('MT_data.db')

    def create_table(self):
        self.db.execute("schema.sql")

    def get_rows_by_timestamp(self, timestamp: str):
        return self.db.execute("SELECT * FROM hr_readings WHERE timestamp = ?", (timestamp,))
    
    def set_row(self, timestamp: str, bpm: int):
        self.db.execute("INSERT INTO hr_readings (timestamp, bpm) VALUES (?, ?)", (timestamp, bpm))

    