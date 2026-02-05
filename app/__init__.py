from flask import Flask
import os
from .config import Config
from .extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)

    # Load default config
    app.config.from_object(Config)

    # Override SECRET_KEY from environment if available
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config.get('SECRET_KEY', 'dev_key_change_this'))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import all models here to ensure relationships are registered
    from app.models.user import User
    from app.models.habit import Habit
    from app.models.habit_completion import HabitCompletion
    from app.models.xp_log import XpLog

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .main import main_bp
    from .auth import auth_bp
    from .habits.routes import habits_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp, url_prefix="/habits")

    return app

