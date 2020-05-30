import email_validator
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Class representing a login form."""
    email = StringField('Email',
                        validators=[
                            Email('Please enter a valid email address'),
                            InputRequired('Please enter your email address')])

    password = PasswordField('Password', [
        InputRequired('Please enter your password')
    ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class EmployeeSignUp(FlaskForm):
    """Class representing an employee sign up form."""
    email = StringField('Email',
                        validators=[
                            Email('Please enter a valid email address'),
                            InputRequired('Please enter your email address')])
    first_name = StringField('First Name',
                             validators=[
                                 InputRequired('Please enter your first name'
                                               )])
    last_name = StringField('Last Name',
                            validators=[
                                InputRequired('Please enter your last name')])

    password = PasswordField('Password',
                             validators=[
                                 InputRequired()])

    confirm_password = PasswordField('Confirm password',
                                     validators=[InputRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')
