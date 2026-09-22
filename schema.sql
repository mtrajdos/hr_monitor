-- Schema for the database

CREATE TABLE IF NOT EXISTS hr_readings (
    sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    bpm INTEGER NOT NULL
)