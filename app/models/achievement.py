from datetime import datetime
from app import db

class Achievement(db.Model):
    __tablename__ = "achievement"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=True)  # Emoji or icon class
    xp_required = db.Column(db.Integer, default=0)  # optional if you want XP-based unlock

    # -----------------------------
    # New fields for sorting/filtering
    # -----------------------------
    type = db.Column(db.String(50), nullable=False, default="completion")  # 'streak', 'level', 'completion', 'xp'
    tier = db.Column(db.Integer, nullable=True)  # used for highest-tier sorting

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    users = db.relationship(
        "UserAchievement",
        back_populates="achievement",
        lazy=True,
        cascade="all, delete-orphan",
    )

