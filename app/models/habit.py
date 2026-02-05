from datetime import datetime, date
from app import db

class Habit(db.Model):
    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # Updated ForeignKey to point to app_user.id
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("app_user.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Streak tracking
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    longest_streak = db.Column(db.Integer, default=0, nullable=False)
    last_completed_date = db.Column(db.Date)

    # Relationships
    user = db.relationship("User", back_populates="habits")
    completions = db.relationship(
        "HabitCompletion",
        back_populates="habit",
        lazy=True,
        cascade="all, delete-orphan",
    )
    xp_logs = db.relationship(
        "XpLog",
        back_populates="habit",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Habit {self.name} | User ID={self.user_id}>"

