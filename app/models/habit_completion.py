from app import db
from datetime import date

class HabitCompletion(db.Model):
    __tablename__ = "habit_completion"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(
        db.Integer,
        db.ForeignKey('habit.id', ondelete='CASCADE'),
        nullable=False
    )
    # Updated ForeignKey to point to app_user.id
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('app_user.id', ondelete='CASCADE'),
        nullable=False
    )
    date = db.Column(db.Date, default=date.today, nullable=False)

    # Relationships
    habit = db.relationship('Habit', back_populates='completions')
    user = db.relationship('User', back_populates='habit_completions')

    def __repr__(self):
        return f"<HabitCompletion habit_id={self.habit_id} user_id={self.user_id} date={self.date}>"

