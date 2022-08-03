from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app.auth import models

from app.admin import forms
from flask.blueprints import Blueprint
from app import db
from datetime import datetime, time
from collections import namedtuple

course_bp = Blueprint('course',  __name__, template_folder='templates', static_folder='static')