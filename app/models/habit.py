from datetime import datetime
from app import db

class Habit(db.Model):
    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

