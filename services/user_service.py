from typing import Any, Dict, Optional

from db.database import get_conn


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT user_id, username, sen_profile, tts_enabled, high_contrast, created_at, updated_at "
            "FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row:
            keys = [column[0] for column in cursor.description]
            return dict(zip(keys, row))
    return None


def list_users() -> list[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT user_id, username, sen_profile, tts_enabled, high_contrast, created_at, updated_at "
            "FROM users ORDER BY user_id"
        )
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]
