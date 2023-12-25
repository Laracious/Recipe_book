from flask import Blueprint, request, jsonify
from recipeapp.models.bookmarks import Bookmark
from recipeapp.utils.data_validation import validate_uuid

bookmark_bp = Blueprint('bookmark', __name__, url_prefix='/api/v1')

@bookmark_bp.route('/bookmarks/create', methods=['POST'])
def create_bookmark():
    """Create a new bookmark and return the result

    Returns:
        JSON: A success or error message
    """
    try:
        data = request.get_json()

        # Validate user_id and recipe_id
        validate_uuid(data.get('user_id'))
        validate_uuid(data.get('recipe_id'))

        bookmark = Bookmark(
            user_id=data.get('user_id'), recipe_id=data.get('recipe_id')
            )
        result = bookmark.create_or_delete_bookmark()

        return jsonify({'message': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookmark_bp.route('/bookmarks/<user_id>', methods=['GET'])
def get_user_bookmarks(user_id):
    """Get all bookmarks for a user

    Args:
        user_id (str): The ID of the user whose bookmarks to retrieve.

    Returns:
        JSON: A list of bookmark objects.
    """
    try:
        # Validate user_id
        validate_uuid(user_id)

        # Find all bookmarks for the user
        bookmarks = Bookmark.find_bookmarks_by_user(user_id)

        # Convert bookmarks to a list of dictionaries
        bookmarks_data = [
            {'recipe_id': bookmark.recipe_id} for bookmark in bookmarks
            ]

        return jsonify({"bookmarks": bookmarks_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
