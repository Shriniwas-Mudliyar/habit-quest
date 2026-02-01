from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Habit, HabitCompletion
from app.habits.forms import HabitForm

habits_bp = Blueprint("habits", __name__, url_prefix="/habits")


@habits_bp.route("/")
@login_required
def list_habits():
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # habits completed today
    completed_today = {
        hc.habit_id
        for hc in HabitCompletion.query.filter_by(
            user_id=current_user.id,
            date=date.today()
        ).all()
    }

    return render_template(
        "habits/list.html",
        habits=habits,
        completed_today=completed_today
    )


@habits_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_habit():
    form = HabitForm()

    if form.validate_on_submit():
        habit = Habit(
            name=form.name.data,
            user_id=current_user.id,
        )
        db.session.add(habit)
        db.session.commit()
        flash("Habit created successfully!", "success")
        return redirect(url_for("habits.list_habits"))

    return render_template("habits/create.html", form=form)


@habits_bp.route("/<int:habit_id>/complete", methods=["POST"])
@login_required
def complete_habit(habit_id):
    already_completed = HabitCompletion.query.filter_by(
        habit_id=habit_id,
        user_id=current_user.id,
        date=date.today()
    ).first()

    if not already_completed:
        completion = HabitCompletion(
            habit_id=habit_id,
            user_id=current_user.id,
            date=date.today()
        )
        db.session.add(completion)
        db.session.commit()
        flash("Habit marked as complete!", "success")

    return redirect(url_for("habits.list_habits"))


@habits_bp.route("/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.filter_by(
        id=habit_id,
        user_id=current_user.id
    ).first_or_404()

    HabitCompletion.query.filter_by(
        habit_id=habit.id,
        user_id=current_user.id
    ).delete()

    db.session.delete(habit)
    db.session.commit()

    flash("Habit deleted.", "info")
    return redirect(url_for("habits.list_habits"))

