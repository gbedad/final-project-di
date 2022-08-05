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


@course_bp.route('/courses/students/course_list/<int:student_id>', methods=['GET', 'POST'])
@login_required
def course_list(student_id):
    courses = models.Course.query.all()
    courses_for_student = []
    student_sel = ''
    for course in courses:
        for stud in course.student:
            if stud.id == student_id:
                student_sel = f"{stud.first_name} {stud.last_name}"
                courses_for_student.append(course)

    return render_template('courses/student_course_list.html', data=courses_for_student, title='Course  list for student', legend=f'Courses of {student_sel}')


@course_bp.route('/courses/tutors/course_list/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def tutor_course_list(tutor_id):
    courses = models.Course.query.all()
    courses_for_tutor = []
    tutor_sel = ''
    for course in courses:
        for tut in course.tutor:
            if tut.id == tutor_id:
                tutor_sel = f"{tut.first_name} {tut.last_name}"
                courses_for_tutor.append(course)

    return render_template('courses/tutor_course_list.html', data=courses_for_tutor, title='Course  list for student', legend=f'Courses of {tutor_sel}')