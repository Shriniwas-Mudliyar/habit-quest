from flask import Blueprint

# Use url_prefix so all routes start with /habits
habits_bp = Blueprint("habits", __name__, url_prefix="/habits", template_folder="templates")

from . import routes

