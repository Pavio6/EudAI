import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "eduai.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"
ENGLISH_SEED_PATH = BASE_DIR / "seed_english.sql"


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


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cursor = conn.execute(f"PRAGMA table_info({table})")
    columns = {row[1] for row in cursor.fetchall()}
    return column in columns


def _run_script(conn: sqlite3.Connection, path: Path) -> None:
    with open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def _apply_migrations(conn: sqlite3.Connection) -> None:
    if not _column_exists(conn, "sessions", "subject"):
        conn.execute("ALTER TABLE sessions ADD COLUMN subject TEXT NOT NULL DEFAULT 'Math'")
    if not _column_exists(conn, "recommendations", "subject"):
        conn.execute("ALTER TABLE recommendations ADD COLUMN subject TEXT")


def _ensure_english_seed(conn: sqlite3.Connection) -> None:
    cursor = conn.execute("SELECT COUNT(*) FROM questions WHERE subject = 'English'")
    english_count = cursor.fetchone()[0]
    if english_count == 0 and ENGLISH_SEED_PATH.exists():
        _run_script(conn, ENGLISH_SEED_PATH)


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
        _apply_migrations(conn)
        _ensure_english_seed(conn)
