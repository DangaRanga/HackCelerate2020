"""The flask server."""
import os
from flask import Flask, render_template, flash, request,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from forms.auth_forms import LoginForm,EmployeeSignUp
from config.config import Config

configuration = Config()
app = Flask(__name__)
configuration.set_config(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html',title='login',form=form)

@app.route('/employee_signup',methods=['GET','POST'])
def employee_signup():
    form = EmployeeSignUp() 
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('employee_signup.html',title='signup',form=form)


if __name__ == '__main__':
    app.run()
