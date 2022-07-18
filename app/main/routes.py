from flask import render_template
from app.main import main_blueprint as main_bp


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html', message='index page')