from flask import Blueprint, request, jsonify
from datetime import timedelta
from recipeapp.models.user import User
from recipeapp.utils.data_validation import (
    validate_email, validate_psswd,
    validate_username, validate_uuid
)
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity, create_refresh_token
)

user_bp = Blueprint('user', __name__, url_prefix='/api/v1')

@user_bp.route('users/all', methods=['GET'])
def get_all_users():
    """Gets all users"""
    try:
        users = User.get_all()

        user_list = [user.format() for user in users]

        return jsonify({'users': user_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_bp.route('/users/signup', methods=['POST'])
def create_user():
    """Registers a new user and returns it"""
    
    try:
        data = request.get_json()
        
        #validat data
        validate_psswd(data.get('password'))
        validate_email(data.get('email'))
        validate_username(data.get('username'))
        
        # Check if the username or email is already registered
        existing_user_email = User.find_one(email=data.get('email'))
        existing_user_username = User.find_one(username=data.get('username'))
        
        if existing_user_email or existing_user_username:
            return jsonify(
                {'error': 'Username or email already registered'}), 400
        
        # Create New user
        new_user = User.create(
            username=data.get('username'),
            full_name=data.get('full_name'),
            email=data.get('email'),
            password= data.get('password')
            )
        
        return jsonify({
            'message': 'User created successfully', 'user': new_user.format()
            }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Finds a user associated with user_id and returns it"""
    try:
        #validate user_id
        validate_uuid(user_id)
        
        user = User.find_one(id=user_id)
        if user:
            return jsonify(user.format())
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a particular User"""
    try:
        #validate user_id
        validate_uuid(user_id)
        
        #get the json data
        data = request.get_json()
        
        # Validate the json data
        validate_psswd(data.get('password'))
        validate_email(data.get('email'))
        validate_username(data.get('username'))
        
        user = User.find_one(id=user_id)

        if user:
            """
            Checks if the updated email or username already exists for
            another user"""
            existed_user_by_email = User.find_one(email=data.get('email'))
            existed_user_by_username = User.find_one(
                username=data.get('username')
                )

            if existed_user_by_email and existed_user_by_email.id != user.id:
                return jsonify(
                    {'error': 'Email already exists for another user'}), 400

            if existed_user_by_username and existed_user_by_username.id != user.id:  # nopep8
                return jsonify({
                    'error': 'Username already exists for another user'}), 400

            # Update the user with the data from the JSON
            user.update(**data)
            user.save()

            return jsonify(
                {'message': 'User updated successfully', 'user': user.format()
                 }
                )
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a particular User"""
    try:
        #validate user_id
        validate_uuid(user_id)
        
        user = User.find_one(id=user_id)
        if user:
            user.delete()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/login', methods=['POST'])
def login():
    """Logs in a user"""
    data = request.get_json()
    user = User.find_one(email=data.get('email'))

    try:
        if user and user.check_password(data.get('password')):
            # Set the expiration time for the access token (e.g., 15 minutes)
            access_token = create_access_token(
                identity=user.username,
                expires_delta=timedelta(minutes=15)
                )
            
            # Set the expiration time for the refresh token (e.g., 7 days)
            refresh_token = create_refresh_token(
                identity=user.username, 
                expires_delta=timedelta(days=7)
                )
            
            return jsonify({
                'message': 'User logged in successfully',
                'token': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }), 200
    except Exception as e:
        # Handle other exceptions (not necessarily JWTError)
        return jsonify({
            'error': f'An error occurred while processing the login: {str(e)}'
            }), 500

    return jsonify({'error': 'Invalid email or password'}), 401