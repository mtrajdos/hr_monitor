from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _ROOT / "data"
_DB_PATH = _DATA_DIR / "HR_data.db"
_SCHEMA_PATH = _ROOT / "db" / "schema.sql"