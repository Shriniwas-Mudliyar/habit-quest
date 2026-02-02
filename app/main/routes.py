from flask import render_template
from flask_login import login_required, current_user
from . import main_bp
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from datetime import date

@main_bp.route("/")
@login_required
def home():
    # Pass current_user to template to show email/name
    return render_template("main/home.html", user=current_user)

@main_bp.route("/health")
def health():
    return {"status": "ok"}


@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Fetch user habits
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Mark if habit is completed today
    for habit in habits:
        habit.completed_today = HabitCompletion.query.filter_by(
            habit_id=habit.id, user_id=current_user.id, date=date.today()
        ).first() is not None

    return render_template(
        "main/dashboard.html",
        user=current_user,
        habits=habits
    )

