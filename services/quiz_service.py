from typing import Any, Dict, List, Optional

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
