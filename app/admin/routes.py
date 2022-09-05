from flask import render_template, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models

from app.admin import forms as ad_forms
from app.course import forms as crs_forms
from app.auth import forms as auth_forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime, time
from collections import namedtuple
from app.utils import get_grade_from_range, check_tuple_in_list

admin_bp = Blueprint('admin',  __name__, template_folder='templates', static_folder='static')


@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    students_in_db = db.session.query(models.Students).count()
    tutors_in_db = models.User.query.filter(models.User.role == 'supervisor').count()
    courses_created = models.Course.query.filter(models.Course.status == 'created').count()
    courses_accepted = models.Course.query.filter(models.Course.status == 'accepted').count()
    courses_total = courses_accepted + courses_created

    return render_template('admin/admin_dashboard.html',tutors=tutors_in_db, students=students_in_db, courses_t=courses_created, courses_a=courses_accepted, total=courses_total, title='Show tutors', legend='Admin Dashboard')


@admin_bp.route('/admin/show_tutors')
@login_required
def show_tutors():
    print(current_user.role)
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    q_first = request.args.get('q_first')
    q_last = request.args.get('q_last')
    q_subject = request.args.get('q_subject')
    q_modality = request.args.get('q_modality')

    if q_first:
        q_first = q_first.title()
        tutors = models.User.query.filter_by(role='supervisor').filter(models.User.first_name.contains(q_first))
    elif q_last:
        q_last = q_last.title()
        tutors = models.User.query.filter_by(role='supervisor').filter(models.User.last_name.contains(q_last))
    elif q_first and q_last:
        q_first = q_first.title()
        q_last = q_last.title()
        tutors = models.User.query.filter_by(role='supervisor').filter(models.User.last_name.contains(q_first)).filter(models.User.last_name.contains(q_last))
    elif q_subject:
        if q_subject == q_subject.upper():
            q_subject = q_subject
        else:
            q_subject = q_subject.title()
        tutors = models.User.query.join(models.Tutoring).filter(models.Tutoring.tutor_subjects.any(subject=q_subject))
    elif q_modality:
        q_modality = q_modality.title()
        tutors = models.User.query.join(models.Tutoring).filter(models.Tutoring.tutor_modalities.any(modality=q_modality))
    else:
        tutors = models.User.query.filter_by(role='supervisor').order_by(models.User.created_at)

    return render_template('admin/show_tutors.html', data=tutors, title='Show tutors', legend='List of tutors')


@admin_bp.route('/admin/tutors/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def get_tutor_by_id(tutor_id):
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))
    status_form = ad_forms.ChangeTutorStatus()
    interview_form = ad_forms.PlanInterview()
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
                tutor_interviews.interview_date = interview_form.interview_date.data.strftime('%Y-%m-%d')
                tutor_interviews.interview_time = interview_form.interview_time.data
                tutor_interviews.interviewer = interview_form.interviewer.data
                tutor_interviews.message = interview_form.message.data
        else:
            update_interviews = models.Interviews(interview_date=interview_form.interview_date.data, interview_time=interview_form.interview_time.data,
                                                  interviewer=interview_form.interviewer.data,
                                                  message=interview_form.message.data, user=selected_tutor)
            selected_tutor.status = '4'
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

    if tutor_interviews and tutor_interviews.interview_time:
        interview_form.interview_date.data = datetime.strptime(tutor_interviews.interview_date, '%Y-%m-%d')
        interview_form.interview_time.data = datetime.strptime(tutor_interviews.interview_time, '%H:%M:%S')
        interview_form.interviewer.data = tutor_interviews.interviewer
        interview_form.message.data = tutor_interviews.message

    return render_template('admin/tutor_view.html', data=selected_tutor, status_form=status_form,
                           interview_form=interview_form, title='View Tutor',
                           legend=f'{selected_tutor.first_name} {selected_tutor.last_name} information')


@admin_bp.route('/admin/students/create', methods=['GET', 'POST'])
@login_required
def create_student():

    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    form = ad_forms.CreateStudentForm()

    if form.validate_on_submit():
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        email = form.email.data
        phone = form.phone.data
        phone_parents = form.phone_parents.data
        street = form.street.data
        city = form.city.data
        zipcode = form.zipcode.data
        school = form.school.data
        grade = form.grade.data
        modality = form.modality.data

        student = models.Students(first_name=first_name, last_name=last_name,
                                  email=email, phone=phone, phone_parents=phone_parents,
                                  street=street, city=city, zipcode=zipcode, school=school,
                                  grade=grade, modality=modality)
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

    return render_template('students/student_list.html', data=students, title='Show Students', legend='Students List')


@admin_bp.route('/admin/student/add_subject/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_subject(student_id):
    form = ad_forms.AddSubjectToStudent()
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
            subj_added = models.SubjectToStudy(subject_name=form.subject.data, subject_owner=student.id)

            db.session.add(subj_added)

            db.session.commit()

    return render_template('students/add_subject_to_student.html', form=form, student=student, title='Add Subject', legend=f"Add Subject to {student.first_name} {student.last_name}")


@admin_bp.route('/admin/student/<int:student_id>/update', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    form = ad_forms.UpdateStudentForm()
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

    return render_template('students/create_student.html', form=form, student=student, title='Update Student', legend=f'Update {student.first_name} {student.last_name}')


@admin_bp.route('/admin/student/subject/<int:subject_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subject = models.SubjectToStudy.query.filter_by(id=subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin.add_subject', student_id=subject.subject_owner))


@admin_bp.route('/admin/student/add_availabilities/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_availabilities(student_id):
    form = ad_forms.AddAvailabilitiesToStudent()
    student = models.Students.query.filter_by(id=student_id).first()

    days_list = []
    for d in student.student_availabilities:
        days_list.append(d.day_possible)

    if request.method == 'POST':

        if form.validate_on_submit:
            d = form.day_possible.data
            if d in days_list:
                flash('This day is  already indicated', 'warning')
                return redirect(url_for('admin.add_availabilities', student_id=student.id))
            f = form.day_time_from.data.strftime('%H:%M')
            t = form.day_time_to.data.strftime('%H:%M')
            day_added = models.Availabilities(day_possible=d, day_time_from=f, day_time_to=t, availability_owner=student.id)

            db.session.add(day_added)

            db.session.commit()

    return render_template('students/add_availabilities_to_student.html', form=form, student=student, title='Add Availability',
                           legend=f"Add Availability to {student.first_name} {student.last_name}")


@admin_bp.route('/admin/student/availabilities/<int:availability_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_availability(availability_id):
    day_selected = models.Availabilities.query.filter_by(id=availability_id).first()
    db.session.delete(day_selected)
    db.session.commit()
    return redirect(url_for('admin.add_availabilities', student_id=day_selected.availability_owner))


@admin_bp.route('/admin/tutor/<int:tutor_id>/view', methods=['GET', 'POST'])
@login_required
def tutor_detailed_view(tutor_id):
    tutor_selected = models.User.query.filter_by(id=tutor_id).first()

    if tutor_selected:
        return render_template('admin/tutor_profile.html', data=tutor_selected, title='Tutor Details', legend='Tutor Details')


@admin_bp.route('/admin/student/<int:student_id>/search_tutor', methods=['GET', 'POST'])
@login_required
def search_tutor(student_id):

    student_selected = models.Students.query.filter_by(id=student_id).first()
    if student_selected.courses:
        for c in student_selected.courses:
            for i in c.tutor:
                check_course = (student_id, i.id, c.subject, c.selected_day)
                # print(student_id, i.id, c.subject)
    else:
        check_course = None

    tutors = models.User.query.filter_by(role='supervisor')
    filtered_grade = student_selected.grade
    filtered_subjects = [x.subject_name for x in student_selected.student_subjects]
    student_filtered_days = [(y.day_possible, y.day_time_from, y.day_time_to) for y in student_selected.student_availabilities]

    create_course_form = crs_forms.CreateCourseForm()
    create_course_form.student.data = student_selected.id

    tutors_list = []
    for tutor in tutors:

        """if student_filtered_days[0][0] == tutor_filtered_days[0][0] and student_filtered_days[0][1] >= tutor_filtered_days[0][1] and \
                student_filtered_days[0][2] <= tutor_filtered_days[0][2]:
            check_day = True"""
        if tutor.tutoring_exp:
            tutor_filtered_days = [(y.day_possible, y.day_time_from, y.day_time_to) for y in
                                   tutor.tutoring_exp.tutor_availabilities]
            #print(tutor_filtered_days)
            for subj in tutor.tutoring_exp.tutor_subjects:
                grade_list = get_grade_from_range(subj.grade_from,  subj.grade_to)
                if subj.subject in filtered_subjects and filtered_grade in grade_list:
                    for availability in student_filtered_days:
                        #print(student_filtered_days)
                        #print(tutor_filtered_days)
                        test_days = check_tuple_in_list(tutor, availability, tutor_filtered_days)
                        #print("test_days", test_days)
                        if len(test_days[0]) > 0:
                            tutors_list.append(tutor)
            tutors_set = set(tutors_list)

    create_course_form.student.data = student_id
    create_course_form.tutor.choices = [(tutor.id, f'{tutor.first_name} {tutor.last_name}') for tutor in tutors_set]

    if request.method == 'POST' and create_course_form.validate_on_submit():
        stud = create_course_form.student.data
        tut = create_course_form.tutor.data
        subj = create_course_form.subject.data
        day = create_course_form.selected_day.data
        start = create_course_form.start_time.data.strftime('%H:%M')
        end = create_course_form.end_time.data.strftime('%H:%M')

        created_course = models.Course(subject=subj, selected_day=day, start_time=start, end_time=end)

        selected_tutor = models.User.query.filter_by(id=tut).first()

        check_existing_course = models.Course.query.filter_by(selected_day=day).filter_by(start_time=start).filter(tutor == selected_tutor)
        if not check_existing_course:
            flash('Course already exist for subject/student/tutor', 'danger')
            return redirect(url_for('course.course_list', student_id=student_selected.id))
        new_course_t = (student_id, selected_tutor.id, subj, day)
        #if check_course is not None:
        if new_course_t == check_course:
            flash('Course already exist', 'danger')
            return redirect(url_for('course.course_list', student_id=student_selected.id))
        created_course.student.append(student_selected)
        created_course.tutor.append(selected_tutor)

        db.session.add(created_course)

        try:

            db.session.commit()
            flash('Course saved to database', 'info')
            return redirect(url_for('course.course_list', student_id=student_selected.id))
        except:
            flash('Something wrong happened', 'warning')
            return redirect(url_for('course.course_list', student_id=student_selected.id))

    return render_template('admin/adequate_tutor_for_student.html', student=student_selected, data=tutors_set, form=create_course_form, title='Show list of possible tutors', legend=f'Matching Tutor(s) for {student_selected.first_name} {student_selected.last_name}')


@admin_bp.route('/admin/courses/show_all')
@login_required
def show_all_courses():
    all_courses = models.Course.query.all()

    return render_template('courses/all_course_list.html', data=all_courses, title ='All Courses', legend='All Courses View')


@admin_bp.route('/admin/user/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role not in ['superadmin', 'admin']:
        flash('Sorry, you have to be an admin', 'warning')
        return redirect(url_for('auth.login'))

    user_form = ad_forms.CreateUserForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        first_name = user_form.first_name.data.title()
        last_name = user_form.last_name.data.title()
        email = user_form.email.data
        role = user_form.role.data if user_form.role.data else "supervisor"
        status = user_form.status.data

        new_user = models.User(username=username, first_name=first_name, last_name=last_name, email=email, role=role, status=status)
        db.session.add(new_user)

        try:
            db.session.commit()
            flash('New user successfully added', 'success')
            return redirect(url_for('admin.show_tutors'))
        except:
            flash('Something wrong happened', 'warning')
            return redirect(url_for('admin.show_tutors'))

    return render_template('admin/create_user.html', user_form=user_form, title='Create User', legend='Create New Tutor')

