from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class OrganizationMasterUpdateForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired(), Length(max=32)])
    add1 = StringField('Address 1*', validators=[
        DataRequired(), Length(max=25)
    ])
    add2 = StringField('Address 2', validators=[Length(max=25)])
    add3 = StringField('Address 3', validators=[Length(max=25)])
    city = StringField('City*', validators=[DataRequired(), Length(max=16)])
    state = StringField('State*', validators=[DataRequired(), Length(max=16)])
    pin = StringField('Pin*', validators=[DataRequired(), Length(max=8)])
    phone = StringField('Phone', validators=[Length(max=16)])
    email = StringField('e-Mail', validators=[
        Optional(), Email(), Length(max=30)
    ])
    submit = SubmitField('Update')
