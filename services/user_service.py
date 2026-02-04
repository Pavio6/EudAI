import sqlite3
from typing import Any, Dict, Optional

from db.database import get_conn


PROFILE_DEFAULTS = {
    "dyslexia": {"tts_enabled": 1, "high_contrast": 1},
    "adhd": {"tts_enabled": 0, "high_contrast": 0},
    "autism": {"tts_enabled": 0, "high_contrast": 1},
    "general": {"tts_enabled": 0, "high_contrast": 0},
    "other": {"tts_enabled": 0, "high_contrast": 0},
}

PROFILE_TIPS = {
    "dyslexia": "Tip: TTS is enabled to support reading.",
    "adhd": "Tip: Take short breaks after a few questions.",
    "autism": "Tip: Clear feedback is provided after each answer.",
    "general": "Tip: You can enable TTS or high contrast in Settings.",
    "other": "Tip: You can enable TTS or high contrast in Settings.",
}


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


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT user_id, username, sen_profile, tts_enabled, high_contrast, created_at, updated_at "
            "FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if row:
            keys = [column[0] for column in cursor.description]
            return dict(zip(keys, row))
    return None


def create_user(username: str, sen_profile: str) -> int:
    cleaned_username = username.strip()
    if not cleaned_username:
        raise ValueError("Username cannot be empty.")

    defaults = PROFILE_DEFAULTS.get(sen_profile, PROFILE_DEFAULTS["general"])
    with get_conn() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO users (username, sen_profile, tts_enabled, high_contrast) "
                "VALUES (?, ?, ?, ?)",
                (
                    cleaned_username,
                    sen_profile,
                    defaults["tts_enabled"],
                    defaults["high_contrast"],
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise ValueError("Username already exists.") from exc
        return cursor.lastrowid


def list_users() -> list[Dict[str, Any]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT user_id, username, sen_profile, tts_enabled, high_contrast, created_at, updated_at "
            "FROM users ORDER BY user_id"
        )
        keys = [column[0] for column in cursor.description]
        return [dict(zip(keys, row)) for row in cursor.fetchall()]


def update_settings(user_id: int, tts_enabled: bool, high_contrast: bool) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET tts_enabled = ?, high_contrast = ? WHERE user_id = ?",
            (1 if tts_enabled else 0, 1 if high_contrast else 0, user_id),
        )


def get_profile_tip(sen_profile: Optional[str]) -> str:
    if not sen_profile:
        return PROFILE_TIPS["general"]
    return PROFILE_TIPS.get(sen_profile, PROFILE_TIPS["general"])
