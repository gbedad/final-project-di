from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TimeField
from wtforms.validators import ValidationError, DataRequired
from ..auth.models import User


STATUS = [('1','created'), ('2','proposed'), ('3', 'documented'), ('4', 'preselected'), ('5', 'selected'), ('6', 'validated')]


class InterviewerChoice(object):
    def __iter__(self):
        sel_interviewers = User.query.filter_by(role='admin')
        choices = [(item.email, f'{item.email}') for item in sel_interviewers]
        for choice in choices:
            yield choice


class ChangeTutorStatus(FlaskForm):
    status = SelectField('Status', choices=STATUS)
    submit = SubmitField('Update')


class PlanInterview(FlaskForm):
    interview_date = DateField('Interview Date', format='%Y-%m-%d')
    interview_time = TimeField('Interview Time', format='%H:%M')
    interviewer = SelectField('Interviewer', choices=InterviewerChoice())
    message = StringField('Short Message')

    submit = SubmitField('Plan Interview')
