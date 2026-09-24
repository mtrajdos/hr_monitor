-- Schema for the database

CREATE TABLE IF NOT EXISTS hr_readings (
    sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    bpm INTEGER NOT NULL,
    acc_x REAL NOT NULL,
    acc_y REAL NOT NULL,
    acc_z REAL NOT NULL
);
