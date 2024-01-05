import os
from flask import Flask, render_template, request, redirect, url_for, current_app, flash, session, jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


from models import db, User


app = Flask(__name__)
CORS(app) # Enable CORS for all routes
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '[``eU6hqGgtsETe/DXykdl%p'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

"""Initialize the database"""
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def laod_user(user_id):
    # return the user object associated with the user_id
    return User.query.get(int(user_id))


"""Index route to serve the react app"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # Serving the HTML file of the React app here, I'm assuming the index page is named 'index.html'
    return send_file('path_to_index_folder/index.html')

# Handle authentication
#########################################
@app.route('/register', methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({'error': 'Invalid request format, JSON expected'}), 400
    
    data = request.get_json() # expecting json data
    # checking if all required fields are present
    required_fields = ['fullname', 'username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    # extract data
    fullname = data.get('fullname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # validations
    # check if any of the required field is missing
    if not fullname or not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    # checking if the length of fullname
    if len(fullname) < 3 or len(fullname) > 50:
        return jsonify({'error': 'Invalid fullname length'}), 400
    # check if username or email already exist
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'Email already exists'}), 400
    
    # create a new user
    new_user = User(
        username=username,
        email=email,
        fullname=fullname,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Invalid request formt, JSON expected'}), 400

        data = request.get_json()
        # check if the required fields are present
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # extract data
        email = data.get('email')
        password = data.get('password')

        # check if the user exists in the database
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # log in user if credentials match the record in the database
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 201
        else:
            # Unauthorized status
            return jsonify({'message': 'Invalid username or password'}), 401
        # Bad request status
    return jsonify({'message': 'Please provide valid credentials'}), 400


@app.route('/profile')
@login_required
def profile():
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'fullname': current_user.fullname
    }

    return jsonify({'user': user_data})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Authentication ends here
################################################

@app.route('/users', methods=['GET'])
def get_all_users():
    # retrieve all users from the database 
    users = User.query.all()

    # make the result JSON
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'fullname': user.fullname
        })

    # return the users as JSON
    return jsonify({'users': user_data})




# Run this only once
with app.app_context():
    db.create_all()
    



if __name__ == '__main__':
    app.run(debug=True)
