from flask import Flask


def create_app():
    flask_app = Flask(__name__)
    from .auth import auth_blueprint as auth_bp
    from .main import main_blueprint as main_bp
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)
    return flask_app


from app.main import routes
