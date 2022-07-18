from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .auth import auth_blueprint as auth_bp
from .main import main_blueprint as main_bp

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)

    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    flask_app.config.from_object(CONFIG_TYPE)

    return flask_app


from app.main import routes
