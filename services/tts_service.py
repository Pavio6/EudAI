import platform
import re
import subprocess
from pathlib import Path

AUDIO_CACHE = Path(__file__).resolve().parent.parent / "assets" / "audio_cache"


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", name)
    cleaned = cleaned.strip("_") or "audio"
    return f"{cleaned}.mp3"


def speak(text: str, cache_key: str) -> str:
    """
    Generate or reuse an mp3 file for the given text.
    Returns the file path. Raises ImportError if gTTS is missing.
    """
    try:
        from gtts import gTTS  # type: ignore
    except ImportError as exc:
        raise ImportError("gTTS not installed") from exc

    AUDIO_CACHE.mkdir(parents=True, exist_ok=True)
    filename = _safe_filename(cache_key)
    filepath = AUDIO_CACHE / filename
    if filepath.exists():
        return str(filepath)

    tts = gTTS(text=text)
    tts.save(str(filepath))
    return str(filepath)


def play(filepath: str) -> None:
    """
    Play an audio file in-process using playsound if available.
    Falls back to a simple system command per platform.
    """
    system = platform.system().lower()

    # On macOS, playsound requires AppKit/pyobjc; prefer the built-in afplay to avoid that dependency.
    if "darwin" in system or "mac" in system:
        _play_fallback(filepath)
        return

    try:
        from playsound import playsound  # type: ignore
        playsound(filepath)
    except ImportError:
        _play_fallback(filepath)
    except Exception:
        # If playsound fails (e.g., missing backend), try OS fallback before surfacing an error.
        _play_fallback(filepath)


def _play_fallback(filepath: str) -> None:
    system = platform.system().lower()
    cmd: list[str] | None = None
    if "darwin" in system or "mac" in system:
        cmd = ["afplay", filepath]
    elif "windows" in system:
        cmd = ["powershell", "-c", f'Start-Process -FilePath \"{filepath}\"']
    else:
        cmd = ["xdg-open", filepath]

    try:
        subprocess.Popen(cmd)
    except Exception as exc:
        raise ImportError("playsound not installed and system playback failed") from exc
