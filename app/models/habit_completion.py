from app.extensions import db
from datetime import date

class HabitCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("habit_id", "date", name="unique_habit_completion_per_day"),
    )

