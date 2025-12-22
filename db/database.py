import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "eduai.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"


def get_conn() -> sqlite3.Connection:
    """Return a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db() -> None:
    """Create tables using schema.sql; safe to run multiple times."""
    with get_conn() as conn, open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def seed_db() -> None:
    """Insert demo data using seed.sql; uses INSERT OR IGNORE for idempotency."""
    with get_conn() as conn, open(SEED_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def _tables_exist(conn: sqlite3.Connection) -> bool:
    """Check if core tables exist."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name IN (?, ?, ?, ?, ?)",
        ("users", "questions", "sessions", "attempts", "recommendations"),
    )
    found = {row[0] for row in cursor.fetchall()}
    required = {"users", "questions", "sessions", "attempts", "recommendations"}
    return required.issubset(found)


def ensure_db_ready() -> None:
    """
    Ensure the database file and tables exist; initialize and seed if needed.
    Runs both init and seed when the file is missing or tables are incomplete.
    """
    needs_setup = not DB_PATH.exists()
    with get_conn() as conn:
        if not needs_setup:
            needs_setup = not _tables_exist(conn)
        if needs_setup:
            init_db()
            seed_db()
