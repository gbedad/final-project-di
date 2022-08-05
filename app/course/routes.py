from flask import render_template, redirect, url_for, flash, request,  render_template_string
from flask_login import current_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models
from app.course import forms as crs_forms
from app.admin import forms as ad_forms
from app.auth import forms as au_forms
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


@course_bp.route('/course/update/<int:course_id>', methods=['GET', 'POST'])
@login_required
def course_update(course_id):
    course_selected = models.Course.query.filter_by(id=course_id).first()
    print(course_selected.student[0].id)
    print(course_selected.tutor[0].id)

    form = crs_forms.CreateCourseForm()

    form.student.data = course_selected.student[0].id
    form.tutor.data = course_selected.tutor[0].id

    form.subject.data = course_selected.subject
    form.selected_day.data = course_selected.selected_day
    form.start_time.data = datetime.strptime(str(course_selected.start_time), "%H:%M:%S")
    form.end_time.data = datetime.strptime(str(course_selected.end_time), "%H:%M:%S")
    form.status.data = course_selected.status

    return render_template('courses/course_update.html', data=course_selected, form=form, title='Course Update', legend='Course Update')


@course_bp.route('/course/delete/<int:course_id>', methods=['GET', 'POST'])
@login_required
def course_delete(course_id):
    course_selected = models.Course.query.filter_by(id=course_id).first()
    print(course_selected.student[0].id)
    student_id = int(course_selected.student[0].id)

    db.session.delete(course_selected)

    try:
        db.session.commit()
        flash('Course deleted', 'info')
        #return redirect(url_for('course.course_list', student_id=course_selected.student[0].id))
    except:
        flash('Something wrong happened', 'danger')
        #return redirect(url_for('course.course_list', student_id=course_selected.student[0].id))

    return redirect(url_for('course.course_list', student_id=student_id))
