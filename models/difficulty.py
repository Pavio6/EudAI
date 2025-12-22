from enum import IntEnum


class DifficultyLevel(IntEnum):
    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5


def clamp_level(level: int) -> DifficultyLevel:
    """Clamp an integer into the supported difficulty range."""
    level = max(DifficultyLevel.VERY_EASY, min(DifficultyLevel.VERY_HARD, level))
    return DifficultyLevel(level)
