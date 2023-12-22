from flask import Blueprint, jsonify, request
from recipeapp.models.recipe import Recipe
#from recipeapp.utils.data_validation import 

recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/v1')


@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    try:
        data = request.get_json()

        # Validate data here if needed

        # Create a new recipe
        new_recipe = Recipe.create(
            name=data.get('name'),
            description=data.get('description'),
            ingredients=data.get('ingredients'),
            instructions=data.get('instructions'),
            user_id=data.get('user_id')
        )

        # Save the new recipe to the database
        #new_recipe.insert()

        return jsonify({
            'message': 'Recipe created successfully',
            'recipe': new_recipe.format()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500