from datetime import datetime
from app import db

class XpLog(db.Model):
    __tablename__ = "xp_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=True)
    xp_amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="xp_logs")
    habit = db.relationship("Habit", back_populates="xp_logs")

    def __repr__(self):
        return f"<XpLog user_id={self.user_id} habit_id={self.habit_id} xp={self.xp_amount} time={self.timestamp}>"

