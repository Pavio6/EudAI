import json
from typing import Any, Dict, List, Optional

from db.database import get_conn


def add_recommendation(
    user_id: int,
    session_id: Optional[int],
    rec_type: str,
    message: str,
    metadata_json: Optional[dict] = None,
) -> int:
    """
    Store a recommendation record.
    Notes:
    - rec_value stores the human-readable message
    - reason stores a JSON payload (e.g., session_id, rule metadata)
    """
    metadata: dict[str, Any] = metadata_json.copy() if metadata_json else {}
    if session_id is not None:
        metadata.setdefault("session_id", session_id)
    reason_payload = json.dumps(metadata, ensure_ascii=True)

    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO recommendations (user_id, rec_type, rec_value, reason) VALUES (?, ?, ?, ?)",
            (user_id, rec_type, message, reason_payload),
        )
        return cursor.lastrowid


def get_latest_recommendations(user_id: int, limit: int = 3) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT rec_id, rec_type, rec_value, reason, created_at "
            "FROM recommendations WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]
