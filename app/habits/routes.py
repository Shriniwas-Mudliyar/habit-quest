from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.forms.habit_form import HabitForm
from app.services.xp_service import add_xp
from datetime import date

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')


@habits_bp.route('/', methods=['GET', 'POST'])
@login_required
def list_habits():
    form = HabitForm()
    if form.validate_on_submit():
        new_habit = Habit(name=form.name.data, user_id=current_user.id)
        db.session.add(new_habit)
        db.session.commit()
        flash('Habit created!', 'success')
        return redirect(url_for('habits.list_habits'))

    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Mark which habits are completed today
    today = date.today()
    completions_today = {c.habit_id for c in HabitCompletion.query.filter_by(user_id=current_user.id, date=today).all()}
    for habit in habits:
        habit.completed_today = habit.id in completions_today

    return render_template('habits/list.html', habits=habits, form=form)


@habits_bp.route('/<int:habit_id>/complete', methods=['POST'])
@login_required
def complete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()
    today = date.today()

    # Check if already completed today
    if HabitCompletion.query.filter_by(habit_id=habit.id, date=today).first():
        flash('Habit already completed today!', 'info')
        return redirect(url_for('habits.list_habits'))

    # Create new completion
    completion = HabitCompletion(habit_id=habit.id, user_id=current_user.id, date=today)
    db.session.add(completion)
    db.session.commit()

    # Add XP
    add_xp(current_user, xp=10, description=f"Completed habit: {habit.name}", habit_id=habit.id)

    flash(f'You completed "{habit.name}" and earned 10 XP!', 'success')
    return redirect(url_for('habits.list_habits'))


@habits_bp.route('/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()

    # Delete completions first (cascade may handle this)
    HabitCompletion.query.filter_by(habit_id=habit.id).delete()
    db.session.delete(habit)
    db.session.commit()
    flash(f'Habit "{habit.name}" deleted.', 'success')
    return redirect(url_for('habits.list_habits'))

