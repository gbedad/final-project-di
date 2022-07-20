from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets,\
    DateField, TextAreaField, validators, IntegerField, IntegerRangeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, NumberRange
from .models import User

CONTRACT_TYPES = [('1', 'Bénévolat'), ('2', 'Service Civique'), ('3', 'Stage'), ('4', 'Autres')]
SCHOOL_SUBJECTS = [('5', 'Mathématiques'), ('6', 'Français'), ('7', 'Anglais'),
                   ('8', 'Espagnol'), ('9', 'Allemand'), ('10', 'SVT'),
                   ('11', 'Physique'),('12', 'Histoire-Géographie'), ('13', 'Géopolitique'),]
SCHOOL_LEVELS = [('1', 'Primaire'), ('2', '6ème'), ('3', '5ème'),
                   ('4', '4ème'), ('5', '3ème'), ('6', 'Seconde'),
                   ('7', 'Première'),('8', 'Terminale'), ('9', 'Sup')]

MODALITIES = [('1', 'Présentiel 12ème'), ('2', 'Présentiel 17ème'), ('3', 'Présentiel Aubervilliers'), ('4', 'Présentiel Autres'), ('5', 'Distanciel'), ('6', 'Hybride')]


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
    phone = StringField('Phone', validators=[DataRequired(), Regexp(regex='^[+-]?[0-9]$')])
    short_text = TextAreaField(u'Please feel free to add any comment', validators=[validators.optional(), validators.length(max=400)])
    birth_date = DateField('Birth Date', format='%d-%m-%Y')
    submit = SubmitField('Save')


class ProfilePage2Form(FlaskForm):
    maths = SelectMultipleField(u'Mathématiques', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))
    physics = SelectMultipleField(u'Physique', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    french = SelectMultipleField(u'Français', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    english = SelectMultipleField(u'Anglais', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    spanish = SelectMultipleField(u'Espagnol', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    svt = SelectMultipleField(u'SVT', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    history = SelectMultipleField(u'Histoire-Géo', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    geopolitics = SelectMultipleField(u'Géopolitique', validators=[DataRequired()], choices=SCHOOL_LEVELS, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    modalities = SelectMultipleField('Modalities', validators=[DataRequired()], choices=MODALITIES, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    availability_days = StringField('Availability Days')
    start_date = DateField('Starting Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Ending Date', format='%Y-%m-%d', validators=[DataRequired()])
    frequency = IntegerField('Freq(h/week)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    company = StringField('Establishment', validators=[DataRequired()])
    activity = StringField('Activity', validators=[DataRequired()])
    contract_type = SelectField(u'Contract Type', validators=[DataRequired()], choices=CONTRACT_TYPES)
    submit = SubmitField('Save')


