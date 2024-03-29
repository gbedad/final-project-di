from flask import render_template, render_template_string, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models
from app.auth import forms
from app.helpers import email
from flask.blueprints import Blueprint
from app import db
from datetime import datetime
from collections import namedtuple
from app.utils import check_field_validity
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth',  __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = forms.LoginForm()
    user = models.User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form, legend='Login')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = forms.RegistrationForm()

    if form.validate_on_submit():
        check_user = models.User.query.filter_by(email=form.email.data).first()
        if check_user:
            flash('This email already existing, login', 'danger')
            return redirect(url_for('auth.register'))
        user = models.User(first_name=form.first_name.data.title(), last_name=form.last_name.data.title(), username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, legend='Welcome to signup page')


@auth_bp.route('/reset_password_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            email.send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form, legend='Request Reset Password')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = models.User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth.index'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, legend='Reset Password')


@auth_bp.route('/user/<user_name>')
@login_required
def profile(user_name):
    user = models.User.query.filter_by(username=user_name).first_or_404()
    return render_template('auth/profile.html', data=user, legend='View Profile')


@auth_bp.route('/user/<user_name>/profile_1', methods=['GET', 'POST'])
@login_required
def profile_1(user_name):
    print('Initial connection to route')
    if current_user.role in ['admin', 'superadmin']:
        user = models.User.query.filter_by(username=user_name).first_or_404()
    else:
        user = current_user.query.filter_by(username=user_name).first_or_404()
    my_infos = user.my_info
    form = forms.ProfilePage1Form()
    if request.method == 'POST':
        if my_infos is not None:
            my_infos.address = request.form["address"]
            my_infos.city = request.form["city"]
            my_infos.zipcode = request.form["zipcode"]
            my_infos.email2 = request.form["email2"]
            my_infos.phone = request.form["phone"]
            my_infos.birth_date = request.form["birth_date"]
            my_infos.short_text = request.form["short_text"]
            try:
                db.session.commit()
                flash('Update successful', 'info')

            except:
                flash('Something went wrong, try again!', 'warning')

        else:
            personal_info = models.MyInformation(address=form.address.data, city=form.city.data,
                                             zipcode=form.zipcode.data, email2=form.email2.data,
                                             phone=form.phone.data, birth_date=form.birth_date.data,
                                             short_text=form.short_text.data, user=user)
            db.session.add(personal_info)
            db.session.commit()
    if my_infos is not None:
        form.address.data = my_infos.address
        form.city.data = my_infos.city
        form.zipcode.data = my_infos.zipcode
        form.email2.data = my_infos.email2
        form.phone.data = my_infos.phone
        form.birth_date.data = datetime.strptime(my_infos.birth_date,'%Y-%m-%d')
        form.short_text.data = my_infos.short_text

    print("Connected to route after update")
    return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
    #return render_template('admin/profile_template.html', data=user, form=form, legend='My Information')


def add_item_to_list(d, ls):
    new_data = []
    result = ""
    for item in ls:
        c = d[item]
        new_data.append(c)
        new_data_as_str = ','.join(new_data)
        result = new_data_as_str
    return result


@auth_bp.route('/user/<user_name>/profile_2', methods=['GET', 'POST'])
@login_required
def profile_2(user_name):
    if current_user.role in ['admin', 'superadmin']:
        user = models.User.query.filter_by(username=user_name).first_or_404()
    else:
        user = current_user.query.filter_by(username=user_name).first_or_404()
    my_tutorate = user.tutoring_exp
    form = forms.ProfilePage2Form()
    availability_form = forms.AddAvailabilitiesToTutor()
    modality_form = forms.AddModalityToTutor()
    subjects_form = forms.AddSubjectGradesToTutor()

    if request.method == 'GET':
        if my_tutorate:
            form.engagement.data = my_tutorate.engagement
            form.frequency.data = my_tutorate.frequency
            form.start_date.data = datetime.strptime(my_tutorate.start_date, '%Y-%m-%d')
            form.end_date.data = datetime.strptime(my_tutorate.end_date, '%Y-%m-%d')
        return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')

    elif request.method == 'POST':

        if subjects_form.validate_on_submit():

            d = subjects_form.subject.data
            f = subjects_form.grade_from.data
            t = subjects_form.grade_to.data

            for item in my_tutorate.tutor_subjects:
                if d == item.subject:
                    flash('Subject already added', 'warning')
                    return redirect(url_for('auth.profile_2', user_name=user.username))
            subject_added = models.SubjectsGrades(subject=d, grade_from=f, grade_to=t,
                                              user_subjects_owner=user.tutoring_exp.id)

            db.session.add(subject_added)

            try:
                db.session.commit()
                flash('Subjects added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        elif availability_form.validate_on_submit():
            d = availability_form.day_possible.data
            f = availability_form.day_time_from.data.strftime('%H:%M')
            t = availability_form.day_time_to.data.strftime('%H:%M')

            for item in my_tutorate.tutor_availabilities:
                if d == item.day_possible:
                    flash('Day already added', 'warning')
                    return redirect(url_for('auth.profile_2', user_name=user.username))
            day_added = models.Availabilities(day_possible=d, day_time_from=f, day_time_to=t,
                                              user_avail_owner=user.tutoring_exp.id)

            db.session.add(day_added)

            try:
                db.session.commit()
                flash('Availabilities added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        elif modality_form.validate_on_submit():
            d = modality_form.modality.data
            for item in my_tutorate.tutor_modalities:
                if d == item.modality:
                    flash('Modality already selected', 'warning')
                    return redirect(url_for('auth.profile_2', user_name=user.username))

            mod_added = models.Modalities(modality=d, user_modality_owner=user.tutoring_exp.id)
            db.session.add(mod_added)

            try:
                db.session.commit()
                flash('Modalities added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        elif form.validate_on_submit():
            if my_tutorate is not None:
                my_tutorate.engagement = form.engagement.data
                my_tutorate.frequency = form.frequency.data
                my_tutorate.start_date = form.start_date.data
                my_tutorate.end_date = form.end_date.data

                try:
                    db.session.commit()
                    flash('Tutoring info added', 'info')
                    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')
                except:
                    flash('Something wrong happened, try again', 'warning')
                    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')
            else:
                added_tutoring = models.Tutoring(engagement=form.engagement.data, frequency=form.frequency.data, start_date=form.start_date.data, end_date=form.end_date.data, user=user)
                db.session.add(added_tutoring)
                db.session.commit()
    if my_tutorate:
        form.engagement.data = my_tutorate.engagement
        form.frequency.data = my_tutorate.frequency
        form.start_date.data = datetime.strptime(my_tutorate.start_date,'%Y-%m-%d')
        form.end_date.data = datetime.strptime(my_tutorate.end_date, '%Y-%m-%d')

    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')


@auth_bp.route('/tutor/availabilities/<int:availability_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_availability(availability_id):
    day_selected = models.Availabilities.query.filter_by(id=availability_id).first()
    avail_owner = day_selected.user_avail_owner
    assoc_tutoring = models.Tutoring.query.filter_by(id=avail_owner).first()
    user = models.User.query.filter_by(id=assoc_tutoring.user_id).first()
    db.session.delete(day_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username if current_user.role =='supervisor' else user.username))


@auth_bp.route('/tutor/modalities/<int:modality_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_modality(modality_id):
    mod_selected = models.Modalities.query.filter_by(id=modality_id).first()
    mod_owner = mod_selected.user_modality_owner
    assoc_tutoring = models.Tutoring.query.filter_by(id=mod_owner).first()
    user = models.User.query.filter_by(id=assoc_tutoring.user_id).first()
    db.session.delete(mod_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username if current_user.role =='supervisor' else user.username))


@auth_bp.route('/tutor/subjects/<int:subject_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subj_selected = models.SubjectsGrades.query.filter_by(id=subject_id).first()
    sub_owner = subj_selected.user_subjects_owner
    assoc_tutoring = models.Tutoring.query.filter_by(id=sub_owner).first()
    user = models.User.query.filter_by(id=assoc_tutoring.user_id).first()
    db.session.delete(subj_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username if current_user.role =='supervisor' else user.username))


@auth_bp.route('/user/<user_name>/profile_3', methods=['GET', 'POST'])
@login_required
def profile_3(user_name):
    if current_user.role in ['admin', 'superadmin']:
        user = models.User.query.filter_by(username=user_name).first_or_404()
    else:
        user = current_user.query.filter_by(username=user_name).first_or_404()
    more_about = user.more
    form3 = forms.ProfilePage3Form()
    if request.method == 'POST' and form3.validate_on_submit():
        if more_about is not None:
            more_about.why = request.form["why"]
            more_about.when = request.form["when"]
            more_about.inquiry = form3.inquiry.data
            more_about.experience = request.form["experience"]

            try:
                db.session.commit()
                flash('Update successful', 'info')
                return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
            except:
                flash('Something went wrong, try again!', 'warning')
                return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
        else:
            update_more = models.MoreAboutMe(why=request.form["why"], when=request.form["when"],
                                             inquiry=request.form["inquiry"], experience=request.form["experience"], user=user)

            if user.tutoring_exp.tutor_availabilities and user.tutoring_exp.tutor_modalities and user.tutoring_exp.tutor_subjects:
                user.status = '3'

            db.session.add(update_more)
            db.session.commit()

    if more_about is not None:
        form3.why.data = more_about.why
        form3.when.data = more_about.when
        form3.inquiry.data = more_about.inquiry
        form3.experience.data = more_about.experience
        print('Found correct route')

    return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
    #return render_template('auth/profile_3.html', data=user, form3=form3, legend='More About Me')


@auth_bp.route('/user/<user_name>/profile_4', methods=['GET', 'POST'])
@login_required
def profile_4(user_name):
    if current_user.role in ['admin', 'superadmin']:
        user = models.User.query.filter_by(username=user_name).first_or_404()
    else:
        user = current_user.query.filter_by(username=user_name).first_or_404()

    form4 = forms.ValidateInterviewDateForm()
    if form4.validate_on_submit():
        user.my_interviews.is_accepted = form4.is_accepted.data
        try:
            db.session.commit()
            if user.my_interviews.is_accepted:
                flash('Interview date accepted', 'info')
            else:
                flash('Interview date declined', 'warning')
        except:
            flash('Something wrong happened, try again', 'warning')

    if user.my_interviews.is_accepted:
        form4.is_accepted.data = user.my_interviews.is_accepted
        print("check where I am", user.my_interviews.is_accepted)

    return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
    #return render_template('auth/profile_4.html', data=user, form=form, legend='My Interviews')


@auth_bp.route('/user/<user_name>/profile_5', methods=['GET', 'POST'])
@login_required
def profile_5(user_name):
    if current_user.role in ['admin', 'superadmin']:
        user = models.User.query.filter_by(username=user_name).first_or_404()
    else:
        user = current_user.query.filter_by(username=user_name).first_or_404()
    #user_uploads = models.Upload.query.all()
    user_uploads = []

    if request.method == 'POST':

        cv_file = request.files['cv_file']
        b3_file = request.files['b3_file']
        ident_file = request.files['id_file']
        print(cv_file, b3_file, ident_file)

        if not cv_file and not b3_file and not ident_file:
            flash('Something wrong  happened or one or more files are missing! Try again.', 'warning')
            return redirect(url_for('auth.profile_5', user_name=user.username))

        cv_f = secure_filename(cv_file.filename)
        b3_f = secure_filename(b3_file.filename)
        id_f = secure_filename(ident_file.filename)
        if b3_f:
            upload_cv = models.UploadCv(cv_filename=cv_f, cv_data=cv_file.read(), user=user)
            db.session.add(upload_cv)
        if cv_f:
            upload_b3 = models.UploadB3(b3_filename=b3_f, b3_data=b3_file.read(), user=user)
            db.session.add(upload_b3)
            user.status = '3'
        if id_f:
            upload_id = models.UploadId(id_filename=id_f, id_data=ident_file.read(), user=user)
            db.session.add(upload_id)

        try:
            db.session.commit()
            flash('Files successfully uploaded', 'success')
            return redirect(url_for('auth.profile_5', user_name=user.username))
        except:
            flash('Something wrong  happened or one or more files are missing! Try again.', 'warning')
            return redirect(url_for('auth.profile_5', user_name=user.username))

    return redirect(url_for('admin.get_tutor_by_id', tutor_id=user.id))
    #return render_template('auth/profile_5.html', data=user, legend='My Commitment')


@auth_bp.route('/user/<int:tutor_id>/dashboard')
@login_required
def tutor_dashboard(tutor_id):
    tutor_sel = models.User.query.filter_by(id=tutor_id).first()
    print(tutor_sel)
    tutor_courses = tutor_sel.courses
    course_num = len(tutor_courses)
    courses = models.Course.query.all()
    my_students = [c.student for c in courses if c.tutor[0] == tutor_sel]
    my_subjects = [c.subject for c in courses if c.tutor[0] == tutor_sel]
    my_students_list = set([s[0].id for s in my_students])
    my_students_num = len(my_students_list)
    my_subjects_num = len(set(my_subjects))
    print(my_subjects_num)

    return render_template('auth/tutor_dashboard.html', data=(tutor_sel, course_num, my_students_num, my_subjects_num, tutor_courses), title='Tutor Dashboard', legend=f'{tutor_sel.first_name} {tutor_sel.last_name} dashboard')
