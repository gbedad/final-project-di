from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets,\
    DateField, TextAreaField, validators, IntegerField, IntegerRangeField, TimeField, TelField, FieldList, FormField, Form
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

INQUIRIES = [('1', 'Je veux aider'), ('2', "Paris je m'engage"), ('3', 'Autres')]

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
    time_from = TimeField('From', validators=[DataRequired()], format='%H:%M')
    time_to = TimeField('To', validators=[DataRequired()], format='%H:%M')


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
    monday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    tuesday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    wednesday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    thursday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    friday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    sunday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    contract_type = SelectField(u'Engagement Type', validators=[DataRequired()], choices=CONTRACT_TYPES)
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


class ProfilePage5Form(FlaskForm):
    pass

