import email_validator
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, ValidationError


class EmployerLoginForm(FlaskForm):
    """Class representing a login form."""
    email = StringField('Email',
                        validators=[
                            Email('Please enter a valid email address'),
                            InputRequired('Please enter your email address')])

    company_name = StringField('Company Name',
                               validators=[
                                   InputRequired()
                               ])
    password = PasswordField('Password',
                             validators=[
                                 InputRequired()])

    submit = SubmitField('Login')


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
                                     validators=[InputRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_employee_email(self, email):
        """Used to validate email"""
        from app import Employee
        employee = Employee.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError(
                'That email address is taken, please choose another.')


class EmployerSignUp(FlaskForm):
    email = StringField('Company Email',
                        validators=[
                            Email('Please enter a valid email address'),
                            InputRequired('Please enter your email address')])

    company_name = StringField('Company Name',
                               validators=[
                                   InputRequired()
                               ])
    password = PasswordField('Password',
                             validators=[
                                 InputRequired()])

    confirm_password = PasswordField('Confirm password',
                                     validators=[InputRequired(),
                                                 EqualTo('password')])

    def validate_employer_email(self, email):
        """Validate email address."""
        from app import Employer
        employee = Employer.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError(
                'That email address is taken, please choose another.')

    class RegisterJobPost(FlaskForm):
        job_title = StringField('Job Title',
                                validators=[
                                    InputRequired()
                                ])
        job_type = StringField('Job Type',
                               validators=[
                                   InputRequired()
                               ])
