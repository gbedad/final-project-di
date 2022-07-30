from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models

from app.admin import forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime, time
from collections import namedtuple

admin_bp = Blueprint('admin',  __name__, template_folder='templates', static_folder='static')


@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    print(current_user.role)
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    return render_template('admin/admin_dashboard.html', title='Show tutors', legend='Admin Dashboard')


@admin_bp.route('/admin/show_tutors')
@login_required
def show_tutors():
    print(current_user.role)
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    tutors = models.User.query.filter_by(role='supervisor')

    return render_template('admin/show_tutors.html', data=tutors, title='Show tutors', legend='List of tutors')


@admin_bp.route('/admin/tutors/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def get_tutor_by_id(tutor_id):
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    status_form = forms.ChangeTutorStatus()
    interview_form = forms.PlanInterview()
    selected_tutor = models.User.query.filter_by(id=tutor_id).first_or_404()
    tutor_interviews = selected_tutor.my_interviews

    if status_form.validate_on_submit():

        selected_tutor.status = status_form.status.data
        try:
            db.session.commit()
            flash('Status Updated successfully', 'success')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))
        except:
            flash('Something wrong happened', 'warning')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))

    elif request.method == 'POST' and interview_form.validate_on_submit():
        if tutor_interviews:

            if tutor_interviews.interview_date is not None or not interview_form.interviewer:
                tutor_interviews.interview_date = datetime.strptime(str(interview_form.interview_date.data), '%Y-%m-%d')
                tutor_interviews.interviewer = interview_form.interviewer.data
                tutor_interviews.message = interview_form.message.data
        else:
            update_interviews = models.Interviews(interview_date=interview_form.interview_date.data,
                                                  interviewer=interview_form.interviewer.data,
                                                  message=interview_form.message.data, user=selected_tutor)
            db.session.add(update_interviews)
            db.session.commit()
        try:
            db.session.commit()
            flash('Interview Planned successfully', 'success')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))
        except:
            flash('Something wrong happened', 'warning')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))
    status_form.status.data = selected_tutor.status

    if tutor_interviews:

        if tutor_interviews.interview_date and interview_form.interviewer:
            interview_form.interview_date.data = datetime.strptime(str(tutor_interviews.interview_date), '%Y-%m-%d %H:%M:%S')

            interview_form.interviewer.data = tutor_interviews.interviewer

            interview_form.message.data = tutor_interviews.message

    return render_template('admin/tutor_view.html', data=selected_tutor, status_form=status_form,
                           interview_form=interview_form, title='View Tutor',
                           legend=f'{selected_tutor.username} information')


@admin_bp.route('/admin/students/create', methods=['GET', 'POST'])
@login_required
def create_student():

    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    form = forms.CreateStudentForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        phone_parents = form.phone_parents.data
        street = form.street.data
        city = form.city.data
        zipcode = form.zipcode.data
        school = form.school.data
        grade = form.grade.data
        modality = form.modality.data
        avail_from = form.avail_from.data
        avail_to = form.avail_to.data

        student = models.Students(first_name=first_name, last_name=last_name,
                                  email=email, phone=phone, phone_parents=phone_parents,
                                  street=street, city=city, zipcode=zipcode, school=school,
                                  grade=grade, modality=modality, avail_from=avail_from,  avail_to=avail_to)
        db.session.add(student)



        try:
            db.session.commit()
            flash('Student successfully added', 'success')
            return redirect(url_for('admin.create_student'))
        except:
            flash('Something happened, try again', 'warning')
            return redirect(url_for('admin.create_student'))

    return render_template('students/create_student.html', form=form, title='Create Student', legend='Create Student')


@admin_bp.route('/admin/student/student_list')
@login_required
def student_list():
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    students = models.Students.query.all()
    for student in students:

        print(student.first_name)

    return render_template('students/student_list.html', data=students, title='Show Students', legend='List of Students')


@admin_bp.route('/admin/student/add_subject/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_subject(student_id):
    form = forms.AddSubjectToStudent()
    student = models.Students.query.filter_by(id=student_id).first()
    subjects_for_student = []

    for s in student.student_subjects:
        subjects_for_student.append(s.subject_name)

    print(subjects_for_student)

    if request.method == 'POST':

        if form.validate_on_submit:
            s = form.subject.data
            print(s)
            if s in subjects_for_student:
                flash('Subject already selected', 'warning')
                return redirect(url_for('admin.add_subject', student_id=student.id))
            subj_added = models.SubjectPossible(subject_name=form.subject.data, subject_owner=student.id)

            db.session.add(subj_added)

            db.session.commit()

    return render_template('students/add_subject_to_student.html', form=form, student=student, title='Add Subject', legend=f"Add Subject to {student.first_name} {student.last_name}")


@admin_bp.route('/admin/student/<int:student_id>/update', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    form = forms.UpdateStudentForm()
    student = models.Students.query.filter_by(id=student_id).first()

    if form.validate_on_submit():
        student.email = form.email.data
        student.phone = form.phone.data
        student.phone_parents = form.phone_parents.data
        student.street = form.street.data
        student.city = form.city.data
        student.zipcode = form.zipcode.data
        student.school = form.school.data
        student.grade = form.grade.data
        student.modality = form.modality.data
        student.avail_from = form.avail_from.data
        student.avail_to = form.avail_to.data
        try:
            db.session.commit()
            flash(f'Student {student.first_name} {student.last_name} updated successfully', 'success')
            return redirect(url_for('admin.student_list'))
        except:
            db.session.commit()
            flash(f'Something wrong happened, try again', 'warning')
            return redirect(url_for('admin.student_list'))

    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.email.data = student.email
    form.phone.data = student.phone
    form.phone_parents.data = student.phone_parents
    form.street.data = student.street
    form.city.data = student.city
    form.zipcode.data = student.zipcode
    form.school.data = student.school
    form.grade.data = student.grade
    form.modality.data = student.modality
    form.avail_from.data = datetime.strptime(student.avail_from, '%H:%M:%S')
    form.avail_to.data = datetime.strptime(student.avail_to, '%H:%M:%S')
    return render_template('students/create_student.html', form=form, student=student, title='Update Student', legend=f'Update {student.first_name} {student.last_name}')


@admin_bp.route('/admin/student/subject/<int:subject_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subject = models.SubjectPossible.query.filter_by(id=subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin.add_subject', student_id=subject.subject_owner))

'''
@admin_bp.route('/admin/tutors/<int:tutor_id>/change_status', methods=['GET', 'POST'])
@login_required
def change_tutor_status(tutor_id):
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    form = forms.ChangeTutorStatus()
    selected_tutor = models.User.query.filter_by(id=tutor_id).first_or_404()
    print(selected_tutor.status)
    if form.validate_on_submit():
        selected_tutor.status = form.status.data
        print(selected_tutor.status)
        try:
            db.session.commit()
            flash('Status changed successfully', 'success')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))
        except:
            flash('Something wrong happened', 'warning')
            return redirect(url_for('admin.get_tutor_by_id', tutor_id=selected_tutor.id))
    form.status.data = selected_tutor.status
    return render_template('admin/status_modal.html', data=selected_tutor, form=form, title='View Tutor')
'''