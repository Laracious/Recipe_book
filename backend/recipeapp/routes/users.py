"""Users routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from recipeapp.models.user import User
from recipeapp.utils.data_validation import validate_uuid
from recipeapp.models.schemas import UserSchema
from recipeapp.utils.emails import promotion_email


user_bp = Blueprint('user', __name__, url_prefix='/api/v1')

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


@user_bp.route('/users/<string:username>/promote', methods=['POST'])
@jwt_required()
def promote_user(username):
    """Promotes a user to admin"""
    
    # Check if the current user is an admin
    if current_user and current_user.super_admin:
    # Find the user to be promoted
        user_to_promote = User.find_one(username=username)
        if not user_to_promote:
            return jsonify({'error': 'User not found.'}), 404

        # Update the user's is_admin field to True
        user_to_promote.update(is_admin=True)
        user_to_promote.save()
        
        # Send a promotion message to the user
        promotion_email(user_to_promote.full_name, user_to_promote.email)

        return jsonify(
            {'message': f'User {username} has been promoted to admin.'}
            ), 200
    return jsonify({'error': 'Access denied. Super Admins only.'}), 403
    