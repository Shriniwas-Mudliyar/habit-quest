from flask import render_template, request
from flask_login import login_required, current_user
from . import main_bp
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.models.user_achievement import UserAchievement
from datetime import date

@main_bp.route("/")
@login_required
def home():
    """Render the home page with current user info."""
    return render_template("main/home.html", user=current_user)


@main_bp.route("/health")
def health():
    """Simple health check endpoint."""
    return {"status": "ok"}


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard with habits and unlocked achievements."""

    # -----------------------------
    # Fetch user habits
    # -----------------------------
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Mark if each habit is completed today
    today = date.today()
    for habit in habits:
        habit.completed_today = HabitCompletion.query.filter_by(
            habit_id=habit.id, user_id=current_user.id, date=today
        ).first() is not None

    # -----------------------------
    # Fetch unlocked achievements (for dashboard preview)
    # -----------------------------
    show_type = request.args.get("achievements", "latest")  # 'latest' or 'highest'

    achievements_query = UserAchievement.query.filter_by(user_id=current_user.id).join(
        UserAchievement.achievement  # Join to Achievement table
    )

    if show_type == "latest":
        achievements_query = achievements_query.order_by(UserAchievement.unlocked_at.desc())
    else:  # highest-tier first
        achievements_query = achievements_query.order_by(
            UserAchievement.achievement.has().tier.desc(),
            UserAchievement.unlocked_at.desc()
        )

    # Limit number shown on dashboard
    achievements = achievements_query.limit(5).all()

    # -----------------------------
    # Render template
    # -----------------------------
    return render_template(
        "main/dashboard.html",
        user=current_user,
        habits=habits,
        achievements=achievements,
        show_type=show_type
    )


@main_bp.route("/achievements")
@login_required
def view_achievements():
    """Render the full achievements page for the current user."""

    # Fetch all achievements for the user
    achievements = UserAchievement.query.filter_by(user_id=current_user.id).join(
        UserAchievement.achievement
    ).order_by(UserAchievement.unlocked_at.desc()).all()

    return render_template(
        "main/achievements.html",
        achievements=achievements
    )

