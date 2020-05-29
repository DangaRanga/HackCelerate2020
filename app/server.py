"""The flask server."""
from datetime import datetime
from flask import Flask, render_template, url_for, redirect
from forms.auth_forms import LoginForm, EmployeeSignUp
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

# -----------------------------------------------------------------------------#
#                          Initialize components
# -----------------------------------------------------------------------------#

config = Config()
app = Flask(__name__)
db = SQLAlchemy(app)
config.set_config(app)

#-----------------------------------------------------------------------------#
#                               Flask Routes
#-----------------------------------------------------------------------------#


@app.route('/')
def index():
    """Route for index.html."""
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', title='login', form=form)


@app.route('/employee_signup', methods=['GET', 'POST'])
def employee_signup():
    form = EmployeeSignUp()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('employee_signup.html', title='signup', form=form)

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
    app.run()
