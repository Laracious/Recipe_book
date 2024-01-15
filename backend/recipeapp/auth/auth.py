from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from random import randint
from datetime import timedelta
from recipeapp.models.user import User
from recipeapp.models.schemas import UserSchema
from recipeapp.models.jwt_blocklist import TokenBlocklist
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, get_jwt, current_user,
    get_jwt_identity, create_refresh_token
)
from recipeapp.utils.emails import (
    welcome_email, send_otp_email, reset_password_otp
)
from recipeapp.utils.data_validation import (
    validate_psswd, validate_email,
    validate_username
)


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')

def generate_otp():
    return randint(100000, 999999)

# Create a new user endpoint
@auth_bp.route('/auth/signup', methods=['POST'])
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


# Verify new user email
@auth_bp.route('/auth/verify_email', methods=['POST'])
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


# Login endpoint
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Logs in a user"""
    # Get the JSON data
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


# Refresh token enpoint
@auth_bp.route('/auth/refresh', methods=['POST'])
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


# Logout endpoint
@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]

        # Add the JTI to the blocklist
        TokenBlocklist.create(jti=jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200

    except Exception as e:
        print(f"Error during logout: {e}")
        return jsonify({'error': 'An error occurred during logout'}), 500


# Reset password endpoint
@auth_bp.route('/auth/reset-password', methods=['POST'])
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
@auth_bp.route('/auth/verify-otp', methods=['POST'])
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
    
@auth_bp.route('/auth/verify_user', methods=['POST'])
@jwt_required()
def send_otp():
    try:
        # Assuming the current_user is available after login
        if not current_user:
            return jsonify({'error': 'User not authenticated'}), 401

        # Validate the email format
        validate_email(current_user.email)
        
        # Check if the user is already verified
        if current_user.verified:
            return jsonify({'message': 'User already verified'}), 200
        
        # Generate OTP, save it in the database and send it
        otp = generate_otp()
        current_user.otp = otp
        current_user.save()
        
        send_otp_email(
            name=current_user.full_name, email=current_user.email, otp=otp)

        return jsonify(
            {'message': 'OTP sent successfully. Check your email.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500