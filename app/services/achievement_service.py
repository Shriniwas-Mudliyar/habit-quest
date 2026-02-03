from app import db
from app.models.achievement import Achievement
from app.models.user_achievement import UserAchievement
from app.models.habit_completion import HabitCompletion
from app.models.habit import Habit
from datetime import date, timedelta

class AchievementService:
    def __init__(self, user):
        self.user = user
        self.new_achievements = []

    def unlock_achievements(self):
        """
        Check all conditions and unlock new achievements for the user.
        Returns a list of newly unlocked achievements.
        """
        self.check_streaks()
        self.check_levels()
        self.check_xp()
        self.check_completions()
        db.session.commit()
        return self.new_achievements

    # -----------------------------
    # 1️⃣ Streak Achievements
    # -----------------------------
    def check_streaks(self):
        # Get all habits
        habits = Habit.query.filter_by(user_id=self.user.id).all()
        for habit in habits:
            streak = habit.current_streak
            if streak >= 3:
                # Award streak achievements every 30-day multiple for long-term
                milestone = streak if streak < 30 else (streak // 30) * 30
                self._award_unique(f"{milestone}-Day Streak", f"🔥 {milestone}-day streak")

    # -----------------------------
    # 2️⃣ Level Achievements
    # -----------------------------
    def check_levels(self):
        level = self.user.level
        milestones = [5, 10, 20, 50]
        # After level 50, increments of 50 until 1000, then increments of 100
        if level > 50:
            milestones += list(range(100, min(level, 1000)+1, 50))
        if level > 1000:
            milestones += list(range(1100, level+1, 100))
        for milestone in milestones:
            if level >= milestone:
                self._award_unique(f"Level {milestone}", f"🌟 Level {milestone}")

    # -----------------------------
    # 3️⃣ XP Achievements
    # -----------------------------
    def check_xp(self):
        xp = self.user.total_xp
        milestones = [50, 100, 250, 500]  # Early XP milestones
        milestones += list(range(500, min(xp, 10000)+1, 500))
        if xp > 10000:
            milestones += list(range(11000, xp+1, 1000))
        for milestone in milestones:
            if xp >= milestone:
                self._award_unique(f"{milestone} XP", f"💎 {milestone} XP")

    # -----------------------------
    # 4️⃣ Completion Achievements
    # -----------------------------
    def check_completions(self):
        total_completions = HabitCompletion.query.filter_by(user_id=self.user.id).count()
        milestones = [1, 10, 30, 50, 100]
        for milestone in milestones:
            if total_completions >= milestone:
                self._award_unique(f"{milestone} Completions", f"🏆 {milestone} habit completions")
        # Full-day complete
        today = date.today()
        habits = Habit.query.filter_by(user_id=self.user.id).all()
        if all(HabitCompletion.query.filter_by(habit_id=h.id, date=today).first() for h in habits) and habits:
            self._award_unique("Full-Day Complete", "✅ Completed all active habits today")

    # -----------------------------
    # Helper method
    # -----------------------------
    def _award_unique(self, name, description=None):
        """
        Award achievement if not already unlocked.
        """
        achievement = Achievement.query.filter_by(name=name).first()
        if not achievement:
            # Create new achievement record if it doesn't exist
            achievement = Achievement(name=name, description=description or name)
            db.session.add(achievement)
            db.session.flush()  # Make sure ID is available

        unlocked = UserAchievement.query.filter_by(
            user_id=self.user.id, achievement_id=achievement.id
        ).first()
        if not unlocked:
            ua = UserAchievement(user_id=self.user.id, achievement_id=achievement.id)
            db.session.add(ua)
            self.new_achievements.append(achievement)

