import os
from flask import Flask, render_template, request, redirect, url_for, current_app, flash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KET'] = '[``eU6hqGgtsETe/DXykdl%p'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


"""Route for home page"""
@app.route('/')
def home():
    # return 'Hello Recipe'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
