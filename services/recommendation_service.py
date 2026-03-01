import json
from typing import Any, Dict, List, Optional

from db.database import get_conn


def add_recommendation(
    user_id: int,
    session_id: Optional[int],
    subject: Optional[str],
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
            "INSERT INTO recommendations (user_id, subject, rec_type, rec_value, reason) VALUES (?, ?, ?, ?, ?)",
            (user_id, subject, rec_type, message, reason_payload),
        )
        return cursor.lastrowid


def get_latest_recommendations(
    user_id: int, limit: int = 3, subject: Optional[str] = None
) -> List[Dict[str, Any]]:
    query = (
        "SELECT rec_id, subject, rec_type, rec_value, reason, created_at "
        "FROM recommendations WHERE user_id = ? "
    )
    params: list[Any] = [user_id]
    if subject:
        query += "AND subject = ? "
        params.append(subject)
    query += "ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    with get_conn() as conn:
        cursor = conn.execute(query, params)
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]
