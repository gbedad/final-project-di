from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets,\
     TextAreaField, validators, IntegerField, IntegerRangeField, TimeField, TelField, FieldList, FormField, Form
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, NumberRange
from wtforms.fields import DateField
from .models import User, Subjects, Grades, Interviews



CONTRACT_TYPES = [('Bénévolat', 'Bénévolat'), ('Service Civique', 'Service Civique'), ('Stage', 'Stage'), ('Autres', 'Autres')]
SCHOOL_SUBJECTS = [('5', 'Mathématiques'), ('6', 'Français'), ('7', 'Anglais'),
                   ('8', 'Espagnol'), ('9', 'Allemand'), ('10', 'SVT'),
                   ('11', 'Physique'),('12', 'Histoire-Géographie'), ('13', 'Géopolitique'),]
SCHOOL_LEVELS = [('Primaire', 'Primaire'), ('6ème', '6ème'), ('5ème', '5ème'),
                   ('4ème', '4ème'), ('3ème', '3ème'), ('Seconde', 'Seconde'),
                   ('Première', 'Première'),('Terminale', 'Terminale'), ('Sup', 'Sup')]

MODALITIES = [('1', 'Présentiel 12ème'), ('2', 'Présentiel 17ème'), ('3', 'Présentiel Aubervilliers'), ('4', 'Présentiel Autres'), ('5', 'Distanciel'), ('6', 'Hybride')]

INQUIRIES = [('Je veux aider', 'Je veux aider'), ("Paris je m'engage", "Paris je m'engage"), ('Autres', 'Autres')]


class SubjectsChoice(object):
    def __iter__(self):
        sel_subjects = Subjects.query.all()
        choices = [(item.id, f'{item.subject}') for item in sel_subjects]
        for choice in choices:
            yield choice


class GradesChoice(object):
    def __iter__(self):
        sel_grades = Grades.query.all()
        choices = [(item.id, f'{item.grade}') for item in sel_grades]
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
    maths = SelectMultipleField(u'Mathématiques', choices=GradesChoice(), coerce=int, option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))
    physics = SelectMultipleField(u'Physique', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    french = SelectMultipleField(u'Français', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    english = SelectMultipleField(u'Anglais', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    spanish = SelectMultipleField(u'Espagnol', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    svt = SelectMultipleField(u'SVT', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    history = SelectMultipleField(u'Histoire-Géo', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    geopolitics = SelectMultipleField(u'Géopolitique', choices=GradesChoice(), coerce=int,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    modalities = SelectMultipleField(u'Modalities', choices=MODALITIES, coerce=str,
                                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    engagement = SelectField(u'Engagement Type', choices=CONTRACT_TYPES)
    availability_days = StringField('Availability Days')
    start_date = DateField('Starting Date', format='%Y-%m-%d')
    end_date = DateField('Ending Date', format='%Y-%m-%d')
    frequency = IntegerField('Freq(h/week)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    monday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    tuesday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    wednesday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    thursday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    friday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)
    sunday = FieldList(FormField(SelectTimeForm), min_entries=1, max_entries=1)

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
    pass

