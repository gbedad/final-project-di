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
    user = models.User.query.filter_by(username=user_name).first_or_404()
    my_tutorate = user.tutoring_exp
    values = dict(form.maths.choices)
    mods = dict(form.modalities.choices)

    if form.validate_on_submit():

        if my_tutorate is not None:

            selected_maths = form.maths.data
            my_maths = add_item_to_list(values, selected_maths)
            selected_physics = form.physics.data
            my_physics = add_item_to_list(values, selected_physics)
            selected_svt = form.svt.data
            my_svt = add_item_to_list(values, selected_svt)
            selected_french = form.french.data
            my_french = add_item_to_list(values, selected_french)
            selected_english = form.english.data
            my_english = add_item_to_list(values, selected_english)
            selected_spanish = form.spanish.data
            my_spanish = add_item_to_list(values, selected_spanish)
            selected_history = form.history.data
            my_history = add_item_to_list(values, selected_history)
            selected_geopolitics = form.geopolitics.data
            my_geopolitics = add_item_to_list(values, selected_geopolitics)

            my_tutorate.maths = my_maths
            my_tutorate.physics = my_physics
            my_tutorate.svt = my_svt
            my_tutorate.french = my_french
            my_tutorate.english = my_english
            my_tutorate.spanish = my_spanish
            my_tutorate.history = my_history
            my_tutorate.geopolitics = my_geopolitics

            selected_modalities = form.modalities.data
            my_modalities = add_item_to_list(mods, selected_modalities)

            my_tutorate.modalities = my_modalities
            my_tutorate.engagement = form.engagement.data
            my_tutorate.frequency = form.frequency.data
            my_tutorate.start_date = form.start_date.data
            my_tutorate.end_date = form.end_date.data

            group = namedtuple('Avail', ['time_from', 'time_to'])

            for field in form.monday:
                my_tutorate.monday = group(field.time_from.data, field.time_to.data )

            print(my_tutorate.engagement)

            try:
                db.session.commit()
                flash('Tutoring info added', 'info')
                return render_template('auth/profile_2.html', data=user, form=form, legend='How I can Help')
            except:
                flash('Something wrong happened, try again', 'warning')
                return render_template('auth/profile_2.html', data=user, form=form, legend='How I can Help')
        else:
            pass
            #added_tutoring = models.Tutoring(maths=request.form['maths'], user=user)
            #db.session.add(added_tutoring)
            #db.session.commit()
        # TODO validate when information is None. With db.session.add().

    if my_tutorate is not None:
        form.engagement.data = my_tutorate.engagement
        form.frequency.data = my_tutorate.frequency
        form.start_date.data = datetime.strptime(my_tutorate.start_date, '%Y-%m-%d')
        form.end_date.data = datetime.strptime(my_tutorate.end_date, '%Y-%m-%d')
        my_list = my_tutorate.modalities.split(',')

        if my_tutorate.modalities:
            form.modalities.data = my_list

            print(form.modalities.data)

    return render_template('auth/profile_2.html', data=user, form=form, legend='How I can Help')


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