import sys
from datetime import datetime
from app.__init__ import db


class Employee(db.Model):
    """Class representing an Employee."""

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)
    profile = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        """Representation of an Employee."""
        return f"Employee('{self.email}','{self.f_name}','{self.l_name}')"

class Employer(db.Model):
    """Class representing an Employer"""

    id = db.Column(db.Integer,primary_key=True)
    company = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    job_post = db.relationship('JobPost',backref='employer',lazy=True)

    def __repr___(self):
        """Representation of an Employer."""
        return f"Employer('{self.email}','{self.company}')"

class JobPost(db.Model):
    """Class representing a JobPost."""
    
    post_no = db.Column(db.Integer,primary_key=True)
    job_title = db.Column(db.String(20),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    post_description = db.Column(db.String(120),nullable=False)
    employer_id = db.Column(db.Integer,db.ForeignKey('employer.id'),nullable=False)

    def __repr__(self):
        """Representation of JobPost."""
        return f"JobPost('{self.job_title}','{self.date_posted})'"


def init_db():
    db.create_all()

if __name__=='__main__':
    init_db