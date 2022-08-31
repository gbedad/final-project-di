import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets,\
     TextAreaField, validators, IntegerField, IntegerRangeField, TimeField, TelField, FieldList, FormField, Form, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, NumberRange
from wtforms.fields import DateField
from .models import User, Subjects, Grades, Interviews, Modalities, SubjectsGrades, Availabilities, ModalitiesPossible, SubjectPossible, Tutoring


CONTRACT_TYPES = [('Bénévolat', 'Bénévolat'), ('Service Civique', 'Service Civique'), ('Stage', 'Stage'), ('Autres', 'Autres')]
SCHOOL_SUBJECTS = [('Mathématiques', 'Mathématiques'), ('Français', 'Français'), ('Anglais', 'Anglais'),
                   ('Espagnol', 'Espagnol'), ('Allemand', 'Allemand'), ('SVT', 'SVT'),
                   ('Physique', 'Physique'),('Histoire-Géographie', 'Histoire-Géographie'), ('Géopolitique', 'Géopolitique'),]
SCHOOL_LEVELS = [('Primaire', 'Primaire'), ('6ème', '6ème'), ('5ème', '5ème'),
                   ('4ème', '4ème'), ('3ème', '3ème'), ('Seconde', 'Seconde'),
                   ('Première', 'Première'),('Terminale', 'Terminale'), ('Sup', 'Sup')]


INQUIRIES = [('Je veux aider', 'Je veux aider'), ("Paris je m'engage", "Paris je m'engage"), ('Autres', 'Autres')]
DAYS = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Sunday', 'Sunday') ]


class ModalitiesChoice(object):
    def __iter__(self):
        sel_modalities = ModalitiesPossible.query.all()
        choices = [(item.modality, f'{item.modality}') for item in sel_modalities]
        for choice in choices:
            yield choice


class SubjectsChoice(object):
    def __iter__(self):
        sel_subjects = SubjectPossible.query.all()
        choices = [(item.subject_name, f'{item.subject_name}') for item in sel_subjects]
        for choice in choices:
            yield choice


class GradesChoice(object):
    def __iter__(self):
        sel_grades = Grades.query.all()
        choices = [(item.grade, f'{item.grade}') for item in sel_grades]
        for choice in choices:
            yield choice


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProfilePage1Form(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    email2 = StringField('Email 2')
    phone = TelField('Phone', validators=[DataRequired()])
    short_text = TextAreaField(u'Please feel free to add any comment', validators=[validators.optional(), validators.length(max=400)])
    birth_date = DateField('Birth Date', format='%Y-%m-%d')
    submit = SubmitField('Save')


class SelectTimeForm(Form):
    time_from = TimeField('From')
    time_to = TimeField('To')


class ProfilePage2Form(FlaskForm):
    engagement = SelectField(u'Engagement Type', choices=CONTRACT_TYPES)
    start_date = DateField('Starting Date', format='%Y-%m-%d')
    end_date = DateField('Ending Date', format='%Y-%m-%d')
    frequency = IntegerField('Freq(h/week)', default=1, validators=[NumberRange(min=1, max=6)])

    submit = SubmitField('Save')


class ProfilePage3Form(FlaskForm):
    why = TextAreaField('Why', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "Why do I apply for such a tutorship mission?"})
    experience = TextAreaField('Experience', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "Do I have already experience of tutorship in the education field?"})
    when = TextAreaField('When', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "When do I want to be contacted?"})
    inquiry = SelectField('How did you learn about us', validators=[DataRequired()], choices=INQUIRIES)
    submit = SubmitField('Save')


class ProfilePage4Form(FlaskForm):
    why = TextAreaField('Why', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "Why do I apply for such a tutorship mission?"})
    experience = TextAreaField('Experience', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "Do I have already experience of tutorship in the education field?"})
    when = TextAreaField('When', validators=[DataRequired(), validators.length(max=400)],
                        render_kw={"placeholder": "When do I want to be contacted?"})
    inquiry = SelectField('How did you learn about us', validators=[DataRequired()], choices=INQUIRIES)
    submit = SubmitField('Save')


class ValidateInterviewDateForm(FlaskForm):
    is_accepted = BooleanField(false_values=(False, 'false', 0, '0'))
    submit = SubmitField('Confirm')


class ProfilePage5Form(FlaskForm):
    cv_filename = FileField('CV File')
    b3_filename = FileField('B3 File')
    id_filename = FileField('ID File')
    submit = SubmitField('Upload')


class AddAvailabilitiesToTutor(FlaskForm):
    day_possible = SelectField(u'Day', choices=DAYS, coerce=str,)
    day_time_from = TimeField(u'Day From', format='%H:%M')
    day_time_to = TimeField(u'Day To', format='%H:%M')

    submit = SubmitField('Add Availability')

    """def validate_day_possible(self, day_possible):
        day_possible_sel = Availabilities.query.filter_by(day_possible=self.day_possible.data).filter_by(user_avail_owner=Tutoring.id).first()
        if day_possible_sel is not None:
            raise ValidationError('Day already selected.')"""


class AddModalityToTutor(FlaskForm):
    modality = SelectField(u'Modality', choices=ModalitiesChoice(), coerce=str)

    submit = SubmitField('Add Modality')

    """def validate_modality(self, modality):
        modality_sel = Modalities.query.filter_by(modality=self.modality.data).first()
        if modality_sel is not None:
            raise ValidationError('Modality already selected.')
"""


class AddSubjectGradesToTutor(FlaskForm):
    subject = SelectField(u'Subject', choices=SubjectsChoice(), coerce=str)
    grade_from = SelectField(u'Grade From', choices=GradesChoice(), coerce=str)
    grade_to = SelectField(u'Grade To', choices=GradesChoice(), coerce=str)

    submit = SubmitField('Add Subject')

    """def validate_subject(self, subject):
        subject_sel = SubjectsGrades.query.filter_by(subject=self.subject.data).filter_by(user_subjects_owner=Tutoring.id).first()
        if subject_sel is not None:
            raise ValidationError('Subject already selected.')"""


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
