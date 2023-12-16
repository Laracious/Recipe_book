import os
from flask import Flask, render_template, request, redirect, url_for, current_app, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from models import db, User


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KET'] = '[``eU6hqGgtsETe/DXykdl%p'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

"""Initialize the database"""
db.init_app(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


"""Route for home page"""
@app.route('/')
def index():
    # return 'Hello Recipe'
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form[password]
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.chech_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


"""Run this only once
with app.app_context():
    db.create_all()
    """



if __name__ == '__main__':
    app.run(debug=True)
