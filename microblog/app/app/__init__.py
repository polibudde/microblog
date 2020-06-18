"""Initialize app."""
from flask import Flask
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

# important stuff for SQLalchemy migrations with foreignkey
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
login_manager = LoginManager()
admini = Admin()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    assets = Environment()
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    admini.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .main import main_routes
        from .auth import auth_routes
        from .admin import admin_routes
        from .api import api_routes
        from .assets import compile_static_assets

        # Create database tables for our data models
        db.create_all()

        # Register Blueprints
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(api_routes.api_bp,url_prefix='/api')

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(assets)

        return app
