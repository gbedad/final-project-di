from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User

CONTRACT_TYPES = [('1', 'Bénévolat'), ('2', 'Service Civique'), ('3', 'Stage'), ('4', 'Prestataire'), ('5', 'Autre')]
SCHOOL_SUBJECTS = [('5', 'Mathématiques'), ('6', 'Français'), ('7', 'Anglais'),
                   ('8', 'Espagnol'), ('9', 'Allemand'), ('10', 'SVT'),
                   ('11', 'Physique'),('12', 'Histoire-Géographie'), ('13', 'Géopolitique'),]
SCHOOL_LEVELS = [('1', 'Primaire'), ('2', '6ème'), ('3', '5ème'),
                   ('4', '4ème'), ('5', '3ème'), ('6', 'Seconde'),
                   ('7', 'Première'),('8', 'Terminale'), ('9', 'Sup')]


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
    phone1 = StringField('Phone 1', validators=[DataRequired()])
    phone2 = StringField('Phone 2')
    company = StringField('Establishment', validators=[DataRequired()])
    activity = StringField('Activity', validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%d-%m-%Y')
    submit = SubmitField('Save')


class ProfilePage2Form(FlaskForm):
    school_subjects = SelectMultipleField(u'School Subjects', validators=[DataRequired()], choices=SCHOOL_SUBJECTS, coerce=str,option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))
    school_levels = SelectMultipleField(u'School Levels', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))
    teaching_terms = StringField('Teaching Terms', validators=[DataRequired()])
    availability_days = StringField('Availability Days')
    avail = StringField('Phone 1', validators=[DataRequired()])
    phone2 = StringField('Phone 2')
    company = StringField('Establishment', validators=[DataRequired()])
    activity = StringField('Activity', validators=[DataRequired()])
    contract_type = SelectField(u'Contract Type', validators=[DataRequired()], choices=CONTRACT_TYPES)
    submit = SubmitField('Save')
