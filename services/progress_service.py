from typing import Any, Dict, List, Optional

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


def get_overall_stats(user_id: int) -> Dict[str, Optional[float]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) AS total_attempts, SUM(is_correct) AS correct_attempts, AVG(time_spent_sec) AS avg_time_spent "
            "FROM attempts WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone() or (0, 0, None)
        total_attempts, correct_attempts, avg_time_spent = row
        accuracy = (correct_attempts or 0) / total_attempts if total_attempts else 0
        return {
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts or 0,
            "accuracy": accuracy,
            "avg_time_spent_sec": avg_time_spent if avg_time_spent is not None else 0,
        }


def get_today_stats(user_id: int) -> Dict[str, int | float]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) AS today_attempts, SUM(is_correct) AS correct_attempts "
            "FROM attempts WHERE user_id = ? AND DATE(created_at) = DATE('now')",
            (user_id,),
        )
        row = cursor.fetchone() or (0, 0)
        today_attempts, correct_attempts = row
        accuracy = (correct_attempts or 0) / today_attempts if today_attempts else 0
        return {
            "today_attempts": today_attempts,
            "today_accuracy": accuracy,
        }


def get_recent_stats(user_id: int, n: int = 10) -> Dict[str, float]:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            SELECT AVG(q.difficulty) AS avg_difficulty,
                   AVG(a.is_correct) AS accuracy
            FROM (
                SELECT question_id, is_correct
                FROM attempts
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ) AS a
            JOIN questions q ON q.question_id = a.question_id
            """,
            (user_id, n),
        )
        row = cursor.fetchone() or (None, None)
        avg_difficulty, accuracy = row
        return {
            "recent_avg_difficulty": avg_difficulty if avg_difficulty is not None else 0,
            "recent_accuracy": accuracy if accuracy is not None else 0,
        }
