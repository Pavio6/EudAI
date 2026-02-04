from typing import Any, Dict, List, Optional, Set, Tuple

from db.database import get_conn


def get_question_by_id(question_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT question_id, subject, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation "
            "FROM questions WHERE question_id = ?",
            (question_id,),
        )
        row = cursor.fetchone()
        if row:
            keys = [column[0] for column in cursor.description]
            return dict(zip(keys, row))
    return None


def get_questions_by_topic(topic: str, limit: int = 10) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT question_id, subject, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation "
            "FROM questions WHERE topic = ? ORDER BY difficulty LIMIT ?",
            (topic, limit),
        )
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]


def start_session(user_id: int) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO sessions (user_id) VALUES (?)",
            (user_id,),
        )
        return cursor.lastrowid


def end_session(session_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE sessions SET ended_at = CURRENT_TIMESTAMP WHERE session_id = ?",
            (session_id,),
        )


def get_random_question(subject: str, difficulty: int, exclude_ids: Set[int]) -> Optional[Dict[str, Any]]:
    query = (
        "SELECT question_id, subject, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation "
        "FROM questions WHERE subject = ? AND difficulty = ?"
    )
    params: list[Any] = [subject, difficulty]
    if exclude_ids:
        placeholders = ",".join("?" for _ in exclude_ids)
        query += f" AND question_id NOT IN ({placeholders})"
        params.extend(list(exclude_ids))
    query += " ORDER BY RANDOM() LIMIT 1"

    with get_conn() as conn:
        cursor = conn.execute(query, params)
        row = cursor.fetchone()
        if row:
            keys = [column[0] for column in cursor.description]
            return dict(zip(keys, row))
    return None


def get_question_with_fallback(
    subject: str, difficulty: int, exclude_ids: Set[int]
) -> Tuple[Optional[Dict[str, Any]], Optional[int]]:
    """
    Try the requested difficulty first; if empty, search nearby difficulties.
    Returns (question, actual_difficulty).
    """
    candidates = [difficulty]
    for delta in range(1, 5):
        if 1 <= difficulty + delta <= 5:
            candidates.append(difficulty + delta)
        if 1 <= difficulty - delta <= 5:
            candidates.append(difficulty - delta)

    for level in candidates:
        question = get_random_question(subject, level, exclude_ids)
        if question:
            return question, level
    return None, None


def record_attempt(
    user_id: int,
    session_id: Optional[int],
    question_id: int,
    selected_option: str,
    is_correct: bool,
    time_spent_sec: int,
    used_tts: bool = False,
) -> int:
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
