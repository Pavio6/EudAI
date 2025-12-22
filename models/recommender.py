from models.difficulty import DifficultyLevel, clamp_level


def next_difficulty(last_was_correct: bool, current_level: int) -> DifficultyLevel:
    """
    Simple adaptive stepper:
    - correct answers move difficulty up one step
    - incorrect answers move difficulty down one step
    - bounds are enforced by clamp_level
    """
    delta = 1 if last_was_correct else -1
    return clamp_level(current_level + delta)
