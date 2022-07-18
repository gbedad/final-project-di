from flask import render_template
from app.auth import auth_blueprint as auth_bp


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html', legend='Welcome to login page')


@auth_bp.route('/register')
def register():
    return render_template('auth/register.html', legend='Welcome to signup page')


@auth_bp.route('/reset_request_password')
def reset_request():
    return render_template('auth/reset_request_password.html', legend='Request Reset Password')


@auth_bp.route('/reset_password')
def rerset_password():
    return render_template('auth/reset_password.html', legend='Reset Password')