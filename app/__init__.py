from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import flask_mail

import os


# login.login_message = _l('Please log in to access this page.')


flask_app = Flask(__name__)
db = SQLAlchemy()
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.ProductionConfig')
flask_app.config.from_object(CONFIG_TYPE)
flask_app.config.from_object(Config)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

flask_app.config["MAIL_SERVER"] = 'smtp.gmail.com'
flask_app.config["MAIL_PORT"] = 587
flask_app.config["MAIL_USE_TLS"] = True
flask_app.config["MAIL_USE_SSL"] = False
flask_app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", None)
flask_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", None)


migrate = Migrate()

mail = flask_mail.Mail(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'auth.login'

db.init_app(flask_app)
migrate.init_app(flask_app, db)

from app.auth.routes import auth_bp
from app.main.routes import main_bp
from app.admin.routes import admin_bp
from app.course.routes import course_bp

flask_app.register_blueprint(auth_bp)
flask_app.register_blueprint(main_bp)
flask_app.register_blueprint(admin_bp)
flask_app.register_blueprint(course_bp)


#from app.main import routes
#from app.auth import routes, forms, models


