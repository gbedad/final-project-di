from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired


STATUS = [('1','created'), ('2','proposed'), ('3', 'documented'), ('4', 'preselected'), ('5', 'selected'), ('6', 'validated')]


class ChangeTutorStatus(FlaskForm):
    status = SelectField('Status', validators=[DataRequired()], choices=STATUS)
    submit = SubmitField('Update')
