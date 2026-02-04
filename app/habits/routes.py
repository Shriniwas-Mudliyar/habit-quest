from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from datetime import date

from app import db
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.forms.habit_form import HabitForm
from app.services.xp_service import add_xp
from app.services.streak_service import update_streak, normalize_streak
from app.services.streak_bonus_service import get_streak_bonus_xp
from app.services.achievement_service import AchievementService

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')


@habits_bp.route('/', methods=['GET', 'POST'])
@login_required
def list_habits():
    form = HabitForm()

    if form.validate_on_submit():
        new_habit = Habit(
            name=form.name.data,
            user_id=current_user.id
        )
        db.session.add(new_habit)
        db.session.commit()
        flash('Habit created!', 'success')
        return redirect(url_for('habits.list_habits'))

    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # 🔁 Normalize streaks (reset if days were missed)
    for habit in habits:
        normalize_streak(habit)

    db.session.commit()

    # Mark which habits are completed today
    today = date.today()
    completions_today = {
        c.habit_id
        for c in HabitCompletion.query.filter_by(
            user_id=current_user.id,
            date=today
        ).all()
    }

    for habit in habits:
        habit.completed_today = habit.id in completions_today

    # Check if any new achievements were unlocked in previous request
    new_achievements = session.pop('new_achievements', [])

    return render_template(
        'habits/list.html',
        habits=habits,
        form=form,
        new_achievements=new_achievements
    )


@habits_bp.route('/<int:habit_id>/complete', methods=['POST'])
@login_required
def complete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()
    today = date.today()

    # Prevent duplicate completion
    if HabitCompletion.query.filter_by(habit_id=habit.id, date=today).first():
        flash('Habit already completed today!', 'info')
        return redirect(url_for('habits.list_habits'))

    # Create completion
    completion = HabitCompletion(
        habit_id=habit.id,
        user_id=current_user.id,
        date=today
    )
    db.session.add(completion)

    # Update streak on completion
    update_streak(habit)

    # Bonus XP for streaks
    bonus_xp = get_streak_bonus_xp(habit.current_streak)
    if bonus_xp:
        add_xp(
            current_user,
            xp=bonus_xp,
            description=f"{habit.current_streak}-day streak bonus",
            habit_id=habit.id
        )

    # Base XP for completion
    add_xp(
        current_user,
        xp=10,
        description=f"Completed habit: {habit.name}",
        habit_id=habit.id
    )

    # Unlock achievements
    achievement_service = AchievementService(current_user)
    new_achievements = achievement_service.unlock_achievements()

    # Store unlocked achievements in session to trigger JS
    if new_achievements:
        session['new_achievements'] = [ach.name for ach in new_achievements]

    db.session.commit()

    flash(f'You completed "{habit.name}" and earned 10 XP!', 'success')
    return redirect(url_for('habits.list_habits'))


@habits_bp.route('/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.filter_by(
        id=habit_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(habit)
    db.session.commit()

    flash(f'Habit "{habit.name}" deleted.', 'success')
    return redirect(url_for('habits.list_habits'))

