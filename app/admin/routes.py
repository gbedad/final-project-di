from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models
from app.auth import forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime
from collections import namedtuple

admin_bp = Blueprint('admin',  __name__, template_folder='templates', static_folder='static')


@admin_bp.route('/admin/show_tutors')
@login_required
def show_tutors():
    print(current_user.role)
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    tutors = models.User.query.filter_by(role='supervisor')

    return render_template('admin/show_tutors.html', data=tutors, title='Show tutors', legend='List of tutors')


@admin_bp.route('/admin/tutors/<int:tutor_id>')
@login_required
def get_tutor_by_id(tutor_id):
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    selected_tutor = models.User.query.filter_by(id=tutor_id).first_or_404()

    return f'{selected_tutor.username}'