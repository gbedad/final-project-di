from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os



# login.login_message = _l('Please log in to access this page.')


flask_app = Flask(__name__)
db = SQLAlchemy()
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
flask_app.config.from_object(CONFIG_TYPE)
flask_app.config.from_object(Config)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate()

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'auth.login'

db.init_app(flask_app)
migrate.init_app(flask_app, db)

from app.auth.routes import auth_bp
from app.main.routes import main_bp

flask_app.register_blueprint(auth_bp)
flask_app.register_blueprint(main_bp)


#from app.main import routes
#from app.auth import routes, forms, models


