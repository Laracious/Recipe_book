from flask import Blueprint, request, jsonify
from models.user import User
from utils.data_validation import validate_email, validate_psswd, validate_username

user_bp = Blueprint('user', __name__, url_prefix='/api/v1')

@user_bp.route('/user', methods=['POST'])
def create_user():
    
    try:
        data = request.get_json()
        
        #validat data
        validate_psswd(data.get('password'))
        validate_email(data.get('email'))
        validate_username(data.get('username'))
        
        # Check if the username or email is already registered
        if User.find_one(
            email=data.get('email')
            ) or User.find_one(username=data('username')):
            return jsonify({'error': 'Username or email already registered'}), 400
        # Create New user
        new_user = User.create(
            username=data.get('username'),
            full_name=data.get('full_name'),
            email=data.get('email'),
            password=User.set_password(data.get('password'))
            )
        return jsonify({'message': 'User created successfully', 'user': new_user.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.find_one(id=user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = User.find_one(id=user_id)
        if user:
            user.update(email=data.get('email'), hashed_password=data.get('hashed_password'))
            return jsonify({'message': 'User updated successfully', 'user': user.to_dict()})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.find_one(id=user_id)
        if user:
            user.delete()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500