"""The flask server."""
from datetime import datetime
from flask import Flask, flash, render_template, url_for, redirect, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from .forms.auth_forms import LoginForm, EmployeeSignUp
from .config.config import Config


# -----------------------------------------------------------------------------#
#                          Initialize components
# -----------------------------------------------------------------------------#

config = Config()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///remoteja.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
config.set_config(app)

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
        flash('Successful login', 'success')
        return redirect(url_for('index'))
    else:
        print(form.validate_on_submit())
    return render_template('login.html', title='login', form=form)


@app.route('/employee-sign', methods=['GET', 'POST'])
def employee_signup():
    form = EmployeeSignUp() if request.method == 'POST' else EmployeeSignUp(request.args)
    if form.validate_on_submit():
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
    return render_template('employee-sign.html', title='signup', form=form)


@app.route('/employeer_sign_up')
def esign():
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


class Employee(db.Model):
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


class Employer(db.Model):
    """Class representing an Employer"""

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    job_post = db.relationship('JobPost', backref='employer', lazy=True)

    def __repr___(self):
        """Representation of an Employer."""
        return f"Employer('{self.email}','{self.company}')"


class JobPost(db.Model):
    """Class representing a JobPost."""

    post_no = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    post_description = db.Column(db.String(120), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey(
        'employer.id'), nullable=False)

    def __repr__(self):
        """Representation of JobPost."""
        return f"JobPost('{self.job_title}','{self.date_posted})'"


# -----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)
