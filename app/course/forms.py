from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from app.auth.forms import SubjectsChoice, DAYS
from app.auth.models import User, Students

COURSE_STATUS = [('created', 'Created'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')]


class TutorsChoice(object):
    def __iter__(self):
        sel_tutors = User.query.filter_by(role='supervisor')
        choices = [(item.id, f'{item.first_name} {item.last_name}') for item in sel_tutors]
        for choice in choices:
            yield choice


class StudentsChoice(object):
    def __iter__(self):
        sel_students = Students.query.all()
        choices = [(item.id, f'{item.first_name} {item.last_name}') for item in sel_students]
        for choice in choices:
            yield choice


class CreateCourseForm(FlaskForm):
    student = SelectField('Student', coerce=int, choices=StudentsChoice())
    tutor = SelectField('Tutor', coerce=str, choices=TutorsChoice())
    subject = SelectField('Field', coerce=str, choices=SubjectsChoice())
    selected_day = SelectField('Day', coerce=str, choices=DAYS)
    start_time = TimeField('Start Time', format='%H:%M')
    end_time = TimeField('End Time', format='%H:%M')
    status = SelectField('Status', coerce=str, choices=COURSE_STATUS)

    submit = SubmitField('Create Course')




