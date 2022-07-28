from flask import render_template, redirect, url_for, flash
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