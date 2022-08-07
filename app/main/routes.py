from flask import render_template, url_for
from flask_login import login_required
from flask.blueprints import Blueprint
from app.auth import models

main_bp = Blueprint('main',  __name__, template_folder='templates', static_folder='static' )


@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    new_supervisors = models.User.query.filter_by(role='supervisor').filter_by(status='1')
    count_new_supervisors = len(list(new_supervisors))
    print(count_new_supervisors)
    return render_template('main/index.html', data=new_supervisors, num=count_new_supervisors, title='Home page')