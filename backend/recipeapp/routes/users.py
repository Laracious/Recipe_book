from random import randint
from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, get_jwt, current_user,
    get_jwt_identity, create_refresh_token
)
from recipeapp.models.jwt_blocklist import TokenBlocklist
from recipeapp.models.user import User
from recipeapp.utils.data_validation import (
    validate_email, validate_psswd,
    validate_username, validate_uuid
)
from werkzeug.security import generate_password_hash, check_password_hash
from recipeapp.models.schemas import UserSchema, UserUpdateSchema
from recipeapp.utils.emails import (
    reset_password_otp, send_otp_email, welcome_email
)


user_bp = Blueprint('user', __name__, url_prefix='/api/v1')

def generate_otp():
    return randint(100000, 999999)

@user_bp.route('/users/all', methods=['GET'])
@jwt_required()
def get_all_users():
    """Gets all users"""
    # Check if the current user is an admin
    if current_user and current_user.is_admin:
        try:
            users = User.get_all()
            # Serialize the list of users using the UserSchema
            user_schema = UserSchema(many=True)
            user_list = user_schema.dump(users)

            return jsonify({'users': user_list})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Access denied. Admins only.'}), 403
 
@user_bp.route('/users/signup', methods=['POST'])
def create_user():
    """Registers a new user and returns it"""
    
    try:
        data = request.get_json()
        
        #validate data are present
        mandatory_fields = ['username', 'full_name', 'email', 'password']
        for field in mandatory_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate data
        validate_psswd(data.get('password'))
        validate_email(data.get('email'))
        validate_username(data.get('username'))
        
        # Check if the username or email is already registered
        existing_user_email = User.find_one(email=data.get('email'))
        existing_user_username = User.find_one(username=data.get('username'))
        
        if existing_user_email or existing_user_username:
            return jsonify(
                {'error': 'Username or email already registered'}), 400
        
        # Create new user
        new_user = User.create(
            username=data.get('username'),
            full_name=data.get('full_name'),
            email=data.get('email'),
            password=data.get('password')
        )

        # generate a 6-digit OTP
        otp = generate_otp()

        # store the OTP in the user's record
        new_user.otp = otp
        new_user.save()

        # send the verification email with the OTP
        send_otp_email(new_user.full_name, new_user.email, otp)
        
        # Serialize the user using the UserSchema
        user_schema = UserSchema()
        serialized_user = user_schema.dump(new_user)
        
        return jsonify({
            'message': 'User created successfully. \
                A verification email has been sent to your email address.\
                    Please check your inbox and follow the instructions.',
            'user': serialized_user
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
 
@user_bp.route('/users/verify_email', methods=['POST'])
def verify_email():
    """Verifies a user's email and sends a welcome email"""

    try:
        data = request.get_json()

        # validate data are present
        mandatory_fields = ['email', 'otp']
        for field in mandatory_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # get the user by email from the database
        user = User.find_one(email=data.get('email'))

        # check if the user exists
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # check if the user is already verified
        if user.verified:
            return jsonify({'message': 'User already verified'}), 200

        # check if the OTP matches
        if user.otp == data.get('otp'):
            # update the user's verified status to True
            user.verified = True
            user.save()
            
            # send the welcome email
            welcome_email(user.full_name, user.email)

            # return a success message
            return jsonify({'message': 'User verified successfully'}), 200
        else:
            # return an error message
            return jsonify({'error': 'Invalid OTP'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
    
# @user_bp.route('/users/signup', methods=['POST'])
# def create_user():
#     """Registers a new user and returns it"""
    
#     try:
#         data = request.get_json()
        
#         #validate data are present
#         mandatory_fields = ['username', 'full_name', 'email', 'password']
#         for field in mandatory_fields:
#             if not data.get(field):
#                 return jsonify({'error': f'{field} is required'}), 400
        
#         # Validate data
#         validate_psswd(data.get('password'))
#         validate_email(data.get('email'))
#         validate_username(data.get('username'))
        
#         # Check if the username or email is already registered
#         existing_user_email = User.find_one(email=data.get('email'))
#         existing_user_username = User.find_one(username=data.get('username'))
        
#         if existing_user_email or existing_user_username:
#             return jsonify(
#                 {'error': 'Username or email already registered'}), 400
        
#         # Create new user
#         new_user = User.create(
#             username=data.get('username'),
#             full_name=data.get('full_name'),
#             email=data.get('email'),
#             password=data.get('password')
#         )
        
#         # Serialize the user using the UserSchema
#         user_schema = UserSchema()
#         serialized_user = user_schema.dump(new_user)
        
#         return jsonify({
#             'message': 'User created successfully', 'user': serialized_user
#         }), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
@user_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Finds a user associated with user_id and returns it"""
    try:
        # validate user_id
        validate_uuid(user_id)
        
        user = User.find_one_with_relationships(id=user_id)
        user_schema = UserSchema()
        if user:
            return jsonify(user_schema.dump(user))
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Updates a particular User"""
    try:
        # Validate user_id
        validate_uuid(user_id)

        # Get the JSON data
        data = request.get_json()

        if 'username' not in data:
            return jsonify({'error': 'Username is required'}), 400

        # Verify the password
        if not current_user.check_password(data.get('password')):
            return jsonify({'error': 'Invalid password'}), 400

        # Check if the updated username already exists for another user
        existing_username = User.find_one(
            username=data.get('username'))
        if existing_username and existing_username.id != current_user.id:
            return jsonify(
                {'error': 'Username already exists for another user'}), 400
        
        # Update the user with the data from the JSON
        current_user.update(
            username=data.get('username'),
            full_name=data.get('full_name')
        )
        current_user.save()

        # Return a success message
        return jsonify({
            'message': 'User updated successfully',
            "user": UserSchema().dump(current_user)
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Deletes a particular User"""

    # Check if the current user is an admin
    if current_user and current_user.is_admin:
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
    
    return jsonify({'error': 'Access denied. Admins only.'}), 403

@user_bp.route('/users/login', methods=['POST'])
def login():
    """Logs in a user"""
    # Validate the json data and check if email and password are present

    data = request.get_json()
    
    # Validate the json data and check if email and password are present
    mandatory_fields = ['email', 'password']
    for field in mandatory_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    user = User.find_one(email=data.get('email'))

    try:
        if user and user.check_password(data.get('password')):
            # Set the expiration time for the access token (e.g., 15 minutes)
            access_token = create_access_token(identity=user.email)
            
            # Set the expiration time for the refresh token
            refresh_token = create_refresh_token(
                identity=user.email,
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

@user_bp.route('/users/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        # Get the identity (username) from the refresh token
        current_user = get_jwt_identity()

        # Generate a new access token
        new_access_token = create_access_token(identity=current_user)

        return jsonify({
            'message': 'Access token refreshed successfully',
            'token': {
                'access_token': new_access_token
            }
        }), 200
    except Exception as e:
        # Handle other exceptions if needed
        return jsonify(
            {'error': f'An error occurred during token refresh: {str(e)}'}
            ), 500

@user_bp.route('/users/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]

        # Add the JTI to the blocklist
        TokenBlocklist.create(jti=jti)
        print(TokenBlocklist.query.all())

        return jsonify({'message': 'Successfully logged out'}), 200

    except Exception as e:
        print(f"Error during logout: {e}")
        return jsonify({'error': 'An error occurred during logout'}), 500


@user_bp.route('/users/<string:username>/promote', methods=['POST'])
@jwt_required()
def promote_user(username):
    current_user = get_jwt_identity()

    # Check if the current user is an admin
    user = User.find_one(user_id=current_user)
    if not user or not user.is_admin:
        return jsonify({'error': 'Access denied. Admins only.'}), 403

    # Find the user to be promoted
    user_to_promote = User.find_one(username=username)
    if not user_to_promote:
        return jsonify({'error': 'User not found.'}), 404

    # Update the user's is_admin field to True
    user_to_promote.update(is_admin=True)

    return jsonify(
        {'message': f'User {username} has been promoted to admin.'}
        ), 200
    

# Endpoint to reset password, input email, generate otp then send to the mail
@user_bp.route('/users/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    user = User.find_one(email=email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    otp = generate_otp()
    user.otp = otp
    user.save()
    reset_password_otp(user.full_name, email, otp)
    return jsonify({'message': 'OTP sent successfully', 'otp': otp}), 200


# Endpoint to verify otp and reset password
@user_bp.route('/users/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')

        # confirm if all the fields are present
        mandatory_fields = ['email', 'otp', 'new_password']
        for field in mandatory_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        user = User.find_one(email=email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        validate_psswd(new_password)

        if user.otp != otp:
            return jsonify({'error': 'Invalid OTP'}), 400

        user.password = generate_password_hash(new_password)
        user.save()
        return jsonify({'message': 'Password reset successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 