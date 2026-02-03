from datetime import date, timedelta

def update_streak(habit):
    today = date.today()

    # First ever completion
    if habit.last_completed_date is None:
        habit.current_streak = 1

    # Completed yesterday → streak continues
    elif habit.last_completed_date == today - timedelta(days=1):
        habit.current_streak += 1

    # Completed today → already handled elsewhere, but safe guard
    elif habit.last_completed_date == today:
        return False  # no streak change

    # Missed a day → reset streak
    else:
        habit.current_streak = 1

    # Update longest streak if needed
    if habit.current_streak > habit.longest_streak:
        habit.longest_streak = habit.current_streak

    habit.last_completed_date = today
    return True

