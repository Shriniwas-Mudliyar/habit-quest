def get_streak_bonus_xp(current_streak):
    """
    Returns bonus XP based on streak milestones.
    Only triggers when milestone is reached.
    """
    if current_streak == 3:
        return 5
    if current_streak == 7:
        return 20
    return 0

