from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models
from app.auth import forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime

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


@auth_bp.route('/user/<user_name>/profile_2', methods=['GET', 'POST'])
@login_required
def profile_2(user_name):
    form = forms.ProfilePage2Form()
    if form.validate_on_submit():
        pass
    user = models.User.query.filter_by(username=user_name).first_or_404()
    return render_template('auth/profile_2.html', data=user, form=form, legend='How I can Help')


@auth_bp.route('/user/<user_name>/profile_3', methods=['GET', 'POST'])
@login_required
def profile_3(user_name):
    form = forms.ProfilePage3Form()
    if form.validate_on_submit():
        pass
    user = models.User.query.filter_by(username=user_name).first_or_404()
    return render_template('auth/profile_3.html', data=user,form=form, legend='More About Me')


@auth_bp.route('/user/<user_name>/profile_4', methods=['GET', 'POST'])
@login_required
def profile_4(user_name):
    form = forms.ProfilePage4Form()
    if form.validate_on_submit():
        pass
    user = models.User.query.filter_by(username=user_name).first_or_404()
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