from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Human-friendly name (used for greetings & UI)
    display_name = db.Column(db.String(50), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    # Gamification
    total_xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    habits = db.relationship(
        "Habit",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    habit_completions = db.relationship(
        "HabitCompletion",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    xp_logs = db.relationship(
        "XpLog",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    # -------------------
    # Auth helpers
    # -------------------
    def set_password(self, password: str):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies the user's password."""
        return check_password_hash(self.password_hash, password)

    # -------------------
    # XP & Level helpers
    # -------------------
    def add_xp(self, amount: int):
        """
        Adds XP to the user and updates the level.
        :param amount: XP points to add
        """
        self.total_xp = (self.total_xp or 0) + amount
        self.update_level()

    def update_level(self):
        """
        Updates the user's level.
        Level increases by 1 every 100 XP.
        """
        self.level = (self.total_xp // 100) + 1

    # -------------------
    # Representation
    # -------------------
    def __repr__(self):
        return f"<User {self.display_name} ({self.email}) | XP={self.total_xp} | Level={self.level}>"

