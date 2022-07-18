from flask import render_template, url_for
from app.main import main_blueprint as main_bp


@main_bp.route('/')
def index():
    return render_template('index.html', message='index page')