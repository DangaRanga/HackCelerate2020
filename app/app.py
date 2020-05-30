"""The flask server."""
import os
from datetime import datetime
from flask import Flask, flash, render_template, url_for, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from .forms.auth_forms import LoginForm, EmployerLoginForm, EmployeeSignUp, EmployerSignUp
from .config.config import Config
from flask_wtf.csrf import CSRFProtect


# -----------------------------------------------------------------------------#
#                          Initialize components
# -----------------------------------------------------------------------------#

config = Config()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///remoteja.db"
secret_key = os.urandom(28)
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(28)
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = secret_key
# Configure db
db = SQLAlchemy(app)
# Configure Bcrypt for password hashw
bcrypt = Bcrypt(app)
config.set_config(app)
# Set up CSRF Protection
csrf = CSRFProtect(app)
# Initialize login manager
login_manager = LoginManager(app)


#-----------------------------------------------------------------------------#
#                               Flask Routes
#-----------------------------------------------------------------------------#


@app.route('/')
@app.route('/home')
def index():
    """Route for index.html."""
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        employer = Employer.query.filter_by(email=form.email.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            # Consider using remember me
            login_user(employee)
            flash('Successful login', 'success')
            return redirect(url_for('jobs'))
            # TODO - Add employees and employers under the same table
            # This is a highly inefficient method of logging in the user
        elif employer and bcrypt.check_password_hash(employer.password, form.password.data):
            login_user(employer)
            flash('Successful login', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password')

    else:
        print(form.validate_on_submit())
        print(form.errors)
    return render_template('login.html', title='login', form=form)


@app.route('/employer-login', methods=['GET', 'POST'])
def employer_login():
    form = EmployerLoginForm()
    if form.validate_on_submit():
        return redirect(url_for('upload_job'))
    else:
        print(form.validate_on_submit())
        print(form.errors)
    return render_template('employer_login.html', form=form, title='employer_login')


@app.route('/employee-sign', methods=['GET', 'POST'])
def employee_signup():
    # form = EmployeeSignUp()
    form = EmployeeSignUp() if request.method == 'POST' else EmployeeSignUp(request.args)
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.data['password']).decode('utf-8')
        employee = Employee(f_name=form.first_name.data,
                            l_name=form.last_name.data,
                            email=form.email.data,
                            password=hashed_password)
        db.session.add(employee)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('index'))
    else:
        print(form.validate())
        print(form.errors)
    return render_template('employee-sign.html', title='signup', form=form)


@app.route('/employeer_sign_up')
def esign():
    form = EmployeeSignUp() if request.method == 'POST' else EmployeeSignUp(request.args)
    if request.method == "POST" and form.validate_on_submit():
        pass

    return render_template('employer-sign.html')


@app.route('/sign-up')
def signup():
    return render_template('sign-up.html')


@app.route('/jobs')
def jobs():
    jobs = [1, 2, 3, 4, 5]
    return render_template('jobs.html', jobs=jobs)


@app.route('/view-job')
def view_job():
    return render_template('view-job.html')


@app.route('/upload-job')
def upload_job():
    return render_template('upload-job.html')

# -----------------------------------------------------------------------------#
#                          Database Models
# -----------------------------------------------------------------------------#


@login_manager.user_loader
def load_employee(user_id):
    return Employee.query.get(int(user_id))


@login_manager.user_loader
def load_employer(user_id):
    return Employer.query.get(int(user_id))

class Employee(db.Model, UserMixin):
    """Class representing an Employee."""

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """Representation of an Employee."""
        return f"Employee('{self.email}','{self.f_name}','{self.l_name}')"


class Employer(db.Model, UserMixin):
    """Class representing an Employer"""

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    job_post = db.relationship('JobPost', backref='employer', lazy=True)

    def __repr___(self):
        """Representation of an Employer."""
        return f"Employer('{self.email}','{self.company}')"


class JobPost(db.Model, UserMixin):
    """Class representing a JobPost."""

    post_no = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(20), nullable=False)
    job_type = db.Column(db.String(15), nullable=False)
    job_category = db.Column(db.String(15), nullable=False)
    job_location = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    job_description = db.Column(db.String(120), nullable=False)
    additional_information = db.Column(db.String(90), nullable=False,
                                       default="No additional information")
    employer_id = db.Column(db.Integer, db.ForeignKey(
        'employer.id'), nullable=False)

    def __repr__(self):
        """Representation of JobPost."""
        return f"JobPost('{self.job_title}','{self.date_posted})'"


# -----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)
