from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login user loader
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import models so migrations see them
    from app import models  # noqa: F401

    # Register blueprints
    from .main import main_bp
    from .auth import auth_bp
    from .habits.routes import habits_bp   # ✅ IMPORT ONCE, FROM routes

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)      # ❌ NO url_prefix here

    return app

