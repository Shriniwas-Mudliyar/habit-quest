from datetime import datetime
from app import db

class UserAchievement(db.Model):
    __tablename__ = "user_achievement"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("app_user.id", ondelete="CASCADE"), nullable=False
    )
    achievement_id = db.Column(
        db.Integer, db.ForeignKey("achievement.id", ondelete="CASCADE"), nullable=False
    )
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    achievement = db.relationship("Achievement", back_populates="users")

