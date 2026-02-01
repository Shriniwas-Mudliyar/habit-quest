from app.extensions import db
from datetime import datetime

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    frequency = db.Column(db.String(20), nullable=True)  # daily/weekly/etc.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    completions = db.relationship("HabitCompletion", backref="habit", lazy=True)

