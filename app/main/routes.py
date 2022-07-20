from flask import render_template, url_for
from flask_login import login_required
from flask.blueprints import Blueprint

main_bp = Blueprint('main',  __name__, template_folder='templates', static_folder='static' )


@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    return render_template('main/index.html', title='Home page')