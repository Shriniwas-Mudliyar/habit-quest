from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth_bp
from .forms import RegisterForm, LoginForm
from app.models.user import User
from app.extensions import db

# ----------------------
# REGISTER
# ----------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# ----------------------
# LOGIN
# ----------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.home"))  # redirect to main home
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form)


# ----------------------
# LOGOUT
# ----------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

