from typing import Any, Dict, List

from db.database import get_conn


def log_attempt(user_id: int, question_id: int, selected_option: str, is_correct: bool, time_spent_sec: int = 0, session_id: int | None = None, used_tts: bool = False) -> int:
    """Insert an attempt record and return its id."""
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO attempts (user_id, session_id, question_id, selected_option, is_correct, time_spent_sec, used_tts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                session_id,
                question_id,
                selected_option,
                1 if is_correct else 0,
                time_spent_sec,
                1 if used_tts else 0,
            ),
        )
        return cursor.lastrowid


def recent_attempts(user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT attempt_id, question_id, selected_option, is_correct, time_spent_sec, used_tts, created_at "
            "FROM attempts WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]
