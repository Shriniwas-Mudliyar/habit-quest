from datetime import date, timedelta


def update_streak(habit):
    """
    Called ONLY when a habit is completed today.
    Applies Duolingo-style streak logic.
    """
    today = date.today()

    # Safety: already completed today → do nothing
    if habit.last_completed_date == today:
        return False

    # First ever completion
    if habit.last_completed_date is None:
        habit.current_streak = 1

    # Completed yesterday → streak continues
    elif habit.last_completed_date == today - timedelta(days=1):
        habit.current_streak += 1

    # Missed one or more days → reset, then start fresh
    else:
        habit.current_streak = 1

    # Update longest streak
    if habit.current_streak > habit.longest_streak:
        habit.longest_streak = habit.current_streak

    habit.last_completed_date = today
    return True


def normalize_streak(habit):
    """
    Called when habits are viewed (GET request).
    Ensures streak is reset if a day was missed.
    """
    if habit.last_completed_date is None:
        habit.current_streak = 0
        return

    days_since = (date.today() - habit.last_completed_date).days

    # Missed at least one full day → streak lost
    if days_since > 1:
        habit.current_streak = 0

