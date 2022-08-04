from flask import render_template, redirect, url_for, flash, request,  render_template_string
from flask_login import current_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models
from app.course import forms
from app.admin import forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime, time


course_bp = Blueprint('course',  __name__, template_folder='templates', static_folder='static')


@course_bp.route('/courses/course_list', methods=['GET', 'POST'])
@login_required
def course_list():
    courses = models.Course.query.all()

    for course in courses:
        for tutor in course.tutor:
            print(tutor.username)

    return render_template('courses/course_list.html', data=courses)