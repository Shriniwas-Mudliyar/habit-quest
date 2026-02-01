from flask import render_template
from flask_login import login_required, current_user
from . import main_bp

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
    return render_template("main/dashboard.html", user=current_user)

