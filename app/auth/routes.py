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

auth_bp = Blueprint('auth',  __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('login'))
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
        user = models.User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, legend='Welcome to signup page')


# TODO forgot and reset password features
@auth_bp.route('/reset_request_password')
def reset_request():
    return render_template('auth/reset_request_password.html', legend='Request Reset Password')


@auth_bp.route('/reset_password')
def reset_password():
    return render_template('auth/reset_password.html', legend='Reset Password')


@auth_bp.route('/user/<user_name>')
@login_required
def profile(user_name):
    user = models.User.query.filter_by(username=user_name).first_or_404()
    return render_template('auth/profile.html', data=user, legend='View Profile')


@auth_bp.route('/user/<user_name>/profile_1', methods=['GET', 'POST'])
@login_required
def profile_1(user_name):
    form = forms.ProfilePage1Form()
    user = current_user.query.filter_by(username=user_name).first_or_404()
    my_infos = user.my_info

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
                return render_template('auth/profile_1.html', form=form, data=user)
            except:
                flash('Something went wrong, try again!', 'warning')
                return render_template('auth/profile_1.html', form=form)
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

    return render_template('auth/profile_1.html', data=user, form=form, legend='My Information')


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
    form = forms.ProfilePage2Form()
    availability_form = forms.AddAvailabilitiesToTutor()
    modality_form = forms.AddModalityToTutor()
    subjects_form = forms.AddSubjectGradesToTutor()
    user = models.User.query.filter_by(username=user_name).first_or_404()
    my_tutorate = user.tutoring_exp

    if request.method == 'POST':

        if availability_form.validate_on_submit():
            d = availability_form.day_possible.data
            f = availability_form.day_time_from.data.strftime('%H:%M')
            t = availability_form.day_time_to.data.strftime('%H:%M')
            day_added = models.Availabilities(day_possible=d, day_time_from=f, day_time_to=t,
                                              user_avail_owner=user.tutoring_exp.id)

            db.session.add(day_added)

            try:
                db.session.commit()
                flash('Availabilities added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        if subjects_form.validate_on_submit():
            d = subjects_form.subject.data
            f = subjects_form.grade_from.data
            t = subjects_form.grade_to.data
            subject_added = models.SubjectsGrades(subject=d, grade_from=f, grade_to=t,
                                              user_subjects_owner=user.tutoring_exp.id)

            db.session.add(subject_added)

            try:
                db.session.commit()
                flash('Subjects added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        if modality_form.validate_on_submit():
            d = modality_form.modality.data
            mod_added = models.Modalities(modality=d, user_modality_owner=user.tutoring_exp.id)

            db.session.add(mod_added)

            try:
                db.session.commit()
                flash('Modalities added', 'info')
            except:
                flash('Something wrong happened', 'warning')

        if form.validate_on_submit():
            print("on the good track")

            if my_tutorate is not None:

                my_tutorate.engagement = form.engagement.data
                my_tutorate.frequency = form.frequency.data
                my_tutorate.start_date = form.start_date.data.strftime('%Y-%m-%d')
                my_tutorate.end_date = form.end_date.data.strftime('%Y-%m-%d')

                try:
                    db.session.commit()
                    flash('Tutoring info added', 'info')
                    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')
                except:
                    flash('Something wrong happened, try again', 'warning')
                    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')
            else:
                pass
                #added_tutoring = models.Tutoring(maths=request.form['maths'], user=user)
                #db.session.add(added_tutoring)
                #db.session.commit()
            # TODO validate when information is None. With db.session.add().

    form.engagement.data = my_tutorate.engagement
    form.frequency.data = my_tutorate.frequency
    form.start_date.data = datetime.strptime(my_tutorate.start_date, '%Y-%m-%d')
    form.end_date.data = datetime.strptime(my_tutorate.end_date, '%Y-%m-%d')

    return render_template('auth/profile_2.html', data=user, form=form, avail_form=availability_form, mod_form=modality_form, subjects_form=subjects_form, legend='How I can Help')


@auth_bp.route('/tutor/availabilities/<int:availability_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_availability(availability_id):
    day_selected = models.Availabilities.query.filter_by(id=availability_id).first()
    db.session.delete(day_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username))


@auth_bp.route('/tutor/modalities/<int:modality_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_modality(modality_id):
    mod_selected = models.Modalities.query.filter_by(id=modality_id).first()
    db.session.delete(mod_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username))


@auth_bp.route('/tutor/subjects/<int:subject_id>/cancel', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subj_selected = models.SubjectsGrades.query.filter_by(id=subject_id).first()
    db.session.delete(subj_selected)
    db.session.commit()
    return redirect(url_for('auth.profile_2', user_name=current_user.username))



@auth_bp.route('/user/<user_name>/profile_3', methods=['GET', 'POST'])
@login_required
def profile_3(user_name):
    form = forms.ProfilePage3Form()
    user = models.User.query.filter_by(username=user_name).first_or_404()
    more_about = user.more
    print(more_about)
    if request.method == 'POST' and form.validate_on_submit():
        if more_about is not None:
            more_about.why = request.form["why"]
            more_about.when = request.form["when"]
            more_about.inquiry = form.inquiry.data
            more_about.experience = request.form["experience"]

            try:
                db.session.commit()
                flash('Update successful', 'info')
                return render_template('auth/profile_3.html', form=form, data=user)
            except:
                flash('Something went wrong, try again!', 'warning')
                return render_template('auth/profile_3.html', form=form)
        else:
            update_more = models.MoreAboutMe(why=request.form["why"], when=request.form["when"],
                                             inquiry=request.form["inquiry"], experience=request.form["experience"], user=user)

            db.session.add(update_more)
            db.session.commit()

    if more_about is not None:
        form.why.data = more_about.why
        form.when.data = more_about.when
        form.inquiry.data = more_about.inquiry
        form.experience.data = more_about.experience

    return render_template('auth/profile_3.html', data=user, form=form, legend='More About Me')


@auth_bp.route('/user/<user_name>/profile_4', methods=['GET', 'POST'])
@login_required
def profile_4(user_name):
    form = forms.ValidateInterviewDateForm()
    user = models.User.query.filter_by(username=user_name).first_or_404()
    if form.validate_on_submit():
        user.my_interviews.is_accepted = form.is_accepted.data
        db.session.commit()
        if user.my_interviews.is_accepted:
            flash( 'Interview date accepted', 'info')
        else:
            flash('Interview date declined', 'warning')

    form.is_accepted.data = user.my_interviews.is_accepted

    return render_template('auth/profile_4.html', data=user, form=form, legend='My Interviews')


@auth_bp.route('/user/<user_name>/profile_5', methods=['GET', 'POST'])
@login_required
def profile_5(user_name):
    form = forms.ProfilePage5Form()
    if form.validate_on_submit():
        pass
    user = models.User.query.filter_by(username=user_name).first_or_404()
    if request.method == 'POST':
        cv_file = request.files['cv_file']
        b3_file = request.files['b3_file']
        id_file = request.files['id_file']
        if cv_file or b3_file or id_file:
            upload_cv = models.Upload(cv_filename=cv_file.filename, cv_data=cv_file.read())
            db.session.add(upload_cv)
            upload_b3 = models.Upload(b3_filename=b3_file.filename, b3_data=b3_file.read())
            db.session.add(upload_b3)
            upload_id = models.Upload(id_filename=id_file.filename, b3_data=id_file.read())
            db.session.add(upload_id)
        db.session.commit()
    return render_template('auth/profile_5.html', data=user, form=form, legend='My Commitment')