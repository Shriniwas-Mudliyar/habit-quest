from app.extensions import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    category = db.Column(db.String(50))
    frequency = db.Column(db.String(20), default="daily")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

