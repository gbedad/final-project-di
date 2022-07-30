from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateTimeField, DateField, TimeField
from wtforms.validators import ValidationError, DataRequired
from ..auth.models import User, Modalities, Students, SubjectPossible
from ..auth.forms import SubjectsChoice, GradesChoice


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
    interviewer = SelectField('Interviewer', choices=InterviewerChoice())
    message = StringField('Short Message')

    submit = SubmitField('Plan Interview')


class ModalitiesChoice(object):
    def __iter__(self):
        sel_modalities = Modalities.query.all()
        choices = [(item.modality, f'{item.modality}') for item in sel_modalities]
        for choice in choices:
            yield choice


class CreateStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email')
    phone = StringField("Student's Phone")
    phone_parents = StringField("Parent's Phone")
    street = StringField('Street')
    city = StringField('City')
    zipcode = StringField('Zipcode')
    school = StringField('School')
    grade = SelectField('Grade', choices=GradesChoice())
    modality = SelectField('Modality', choices=ModalitiesChoice())
    avail_from = TimeField('Avail From', format='%H:%M')
    avail_to = TimeField('Avail To', format='%H:%M')

    submit = SubmitField('Create Student')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        student = Students.query.filter_by(first_name=self.first_name.data, last_name=self.last_name.data).first()
        if student is not None:
            self.first_name.errors.append(f'{self.first_name.data} {self.last_name.data} already exist in database')
            return False

        return True


class UpdateStudentForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    phone = StringField("Student's Phone")
    phone_parents = StringField("Parent's Phone")
    street = StringField('Street')
    city = StringField('City')
    zipcode = StringField('Zipcode')
    school = StringField('School')
    grade = SelectField('Grade', choices=GradesChoice())
    modality = SelectField('Modality', choices=ModalitiesChoice())
    avail_from = TimeField('Avail From', format='%H:%M')
    avail_to = TimeField('Avail To', format='%H:%M')

    submit = SubmitField('Update Student')


class AddSubjectToStudent(FlaskForm):
    subject = SelectField('Subject', choices=SubjectsChoice(), validators=[DataRequired()])

    submit = SubmitField('Add Subject')

    def validate_subject_name(self, subject_name):
        subject = SubjectPossible.query.filter_by(subject_name=self.subject_name.data).first()
        if subject:
            raise ValidationError('Subject already selected.')
