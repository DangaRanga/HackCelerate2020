import email_validator
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField,  SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, ValidationError, Length


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
        """Used to validate email."""

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
        employer = Employer.query.filter_by(email=email.data).first()
        if employer:
            raise ValidationError(
                'That email address is taken, please choose another.')


class RegisterJobPost(FlaskForm):
    """Class representing a job post."""

    company = StringField('Company',
                          validators=[InputRequired()])
    job_title = StringField('Job Title',
                            validators=[
                                InputRequired()
                            ])
    job_location = StringField('Job location',
                               validators=[
                                   InputRequired(),
                               ])
    job_type = SelectField('Job Type',
                           choices=[
                               ('full-time', 'Full Time'),
                               ('part-time', 'Part Time'),
                               ('remote', 'Remote'),
                               ('contract', 'Contract')
                           ])
    job_category = SelectField('Job Category',
                               choices=[
                                   ('health', 'Health'),
                                   ('technology', 'Technology'),
                                   ('agriculture', 'Agriculture'),
                                   ('retail', 'Retail'),
                                   ('cus-services', 'Customer Services')
                               ])
    job_description = TextAreaField('Enter a short description of the job', render_kw={
        "rows": 8, "cols": 50
    })
    additional_information = TextAreaField('Enter additional information', render_kw={
        "rows": 8, "cols": 50
    })
    submit = SubmitField('Submit Job')
