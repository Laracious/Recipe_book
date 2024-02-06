from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from recipeapp.models.recipe import Recipe
from recipeapp.utils.data_validation import validate_uuid
from recipeapp import db
from flask_jwt_extended import current_user
from recipeapp.models.schemas import RecipeSchema

recipe_bp = Blueprint('recipe', __name__, url_prefix='/api/v1')


@recipe_bp.route('/recipes/create', methods=['POST'])
@jwt_required()
def create_recipe():
    """Creates a new recipe and returns it

    Returns:
        JSON: A list of newly created recipe
    """
    # Check if the current user is an admin
    if current_user and current_user.is_admin:
        try:
            # Validate incoming JSON data against the Marshmallow schema
            data = request.get_json()
            recipe_schema = RecipeSchema()
            errors = recipe_schema.validate(data)

            if errors:
                return jsonify({'error': 'Invalid input data', 'errors': errors}), 400

            # Check for an existing recipe
            existing_recipe = Recipe.find_one(name=data.get('name'))

            if existing_recipe:
                return jsonify({'error': 'Recipe already exists'}), 400

            # Deserialize the validated data using the Marshmallow schema
            new_recipe_data = recipe_schema.load(data)

            # Create a new recipe
            new_recipe = Recipe.create(
                name=new_recipe_data['name'],
                description=new_recipe_data['description'],
                ingredients=new_recipe_data['ingredients'],
                instructions=new_recipe_data['instructions'],
                user_id=current_user.id,
                video=new_recipe_data['video'],
                user_rating=new_recipe_data['user_rating'],
                image=new_recipe_data['image']
            )

            # Serialize the newly created recipe using the Marshmallow schema
            serialized_recipe = recipe_schema.dump(new_recipe)

            # Return the newly created recipe
            return jsonify({
                'message': 'Recipe created successfully',
                'recipe': serialized_recipe
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Access denied. Admins only.'}), 403


@recipe_bp.route('/recipes/<recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """
    Update Recipe

    Update an existing recipe by providing its ID and the updated details
    in the request body.

    Args:
        recipe_id (str): The ID of the recipe to update.

    Returns:
        JSON: A success message indicating that the recipe was updated.
    """
    if current_user and current_user.is_admin:
        try:
            # Validate the recipe_id
            validate_uuid(recipe_id)

            # Get the JSON data from the request
            data = request.get_json()
            
            # Validate incoming JSON data against the Marshmallow schema
            recipe_schema = RecipeSchema()
            errors = recipe_schema.validate(data)
            
            if errors:
                return jsonify(
                    {'error': 'Invalid input data', 'errors': errors}), 400

            # Find the recipe in the database
            recipe = Recipe.find_one(id=recipe_id)

            if not recipe:
                return jsonify({'error': 'Recipe not found'}), 404

            # Check if the updated name already exists for other recipes
            existing_recipe = Recipe.find_one(name=data.get('name'))

            if existing_recipe and existing_recipe.id != recipe.id:
                return jsonify(
                    {'error': 'Recipe name already exists for another recipe'}
                    ), 400

            # Update the recipe with the data from the JSON
            recipe.update(**data)
            recipe.save()
            
            # Serialize the updated recipe using the Marshmallow schema
            serialized_recipe = recipe_schema.dump(recipe)
            
            return jsonify({
                'message': 'Recipe updated successfully',
                'recipe': serialized_recipe
                })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Access denied. Admins only.'}), 403

@recipe_bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_one_recipe(recipe_id):
    """
    Get One Recipe

    Retrieve details of a specific recipe by providing its ID.

    Args:
        recipe_id (str): The ID of the recipe to retrieve.

    Returns:
        JSON: Details of the specified recipe.
    """
    try:
        # Validate the recipe_id
        validate_uuid(recipe_id)

        # Find the recipe in the database
        recipe = Recipe.find_one(id=recipe_id)

        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        # Serialize the recipe using the Marshmallow schema
        recipe_schema = RecipeSchema()
        serialized_recipe = recipe_schema.dump(recipe)

        # Return details of the recipe as JSON
        return jsonify({'recipe': serialized_recipe}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recipe_bp.route('/recipes/all', methods=['GET'])
def get_all_recipes():
    """
    Get All Recipes with Pagination

    Retrieve a paginated list of all recipes.

    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Number of items per page (default: 10)

    Returns:
        JSON: Paginated list of recipe objects.
    """
    try:
        # Parse query parameters for pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Fetch paginated recipes from the database
        recipes = Recipe.query.paginate(
            page=page, per_page=per_page, error_out=False)

        # Serialize the paginated recipes using the Marshmallow schema
        recipe_schema = RecipeSchema(many=True)
        serialized_recipes = recipe_schema.dump(recipes.items)

        # Return the paginated list of recipes as JSON
        return jsonify({
            "recipes": serialized_recipes,
            "page": page,
            "per_page": per_page,
            "total_items": recipes.total,
            "total_pages": recipes.pages
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipe_bp.route('/recipes/<recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """
    Delete Recipe

    Delete a recipe from the database based on the provided recipe_id.

    Args:
        recipe_id (str): The ID of the recipe to delete.

    Returns:
        JSON: A success message indicating that the recipe was deleted.
    """
    if current_user and current_user.is_admin:
        try:
            # Validate the recipe_id
            validate_uuid(recipe_id)

            # Find the recipe in the database
            recipe = Recipe.find_one(id=recipe_id)

            if not recipe:
                return jsonify({'error': 'Recipe not found'}), 404
            # Delete the recipe from the database
            recipe.delete()

            # Return a success message
            return jsonify({'message': 'Recipe deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Access denied. Admins only.'}), 403

@recipe_bp.route('/recipes/<recipe_id>/r_positive', methods=['POST'])
def rate_positive(recipe_id):
    """
    Increment positive user rating for a recipe.

    Args:
        recipe_id (str): The ID of the recipe to rate.

    Returns:
        JSON: A success message indicating that the rating was incremented.
    """
    try:
        # Validate the recipe_id
        validate_uuid(recipe_id)

        # Find the recipe in the database
        recipe = Recipe.find_one(id=recipe_id)

        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404

        # Use the method to increment positive rating
        recipe.add_positive_rating()

        # Commit the changes to the database
        db.session.merge(recipe)
        db.session.commit()

        # Return a success message
        return jsonify(
            {'message': 'Positive rating incremented successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recipe_bp.route('/recipes/<recipe_id>/r_negative', methods=['POST'])
def rate_negative(recipe_id):
    """
    Increment negative user rating for a recipe.

    Args:
        recipe_id (str): The ID of the recipe to rate.

    Returns:
        JSON: A success message indicating that the rating was incremented.
    """
    try:
        # Validate the recipe_id
        validate_uuid(recipe_id)

        # Find the recipe in the database
        recipe = Recipe.find_one(id=recipe_id)

        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404

        # Use the method to increment negative rating
        recipe.add_negative_rating()
        
        # Commit the changes to the database
        db.session.merge(recipe)
        db.session.commit()

        # Return a success message
        return jsonify(
            {'message': 'Negative rating incremented successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@recipe_bp.route('/recipes/<recipe_id>/reset_rating', methods=['POST'])
@jwt_required()
def reset_rating(recipe_id):
    """
    Reset user rating for a recipe.

    Args:
        recipe_id (str): The ID of the recipe to reset the rating.

    Returns:
        JSON: A success message indicating that the rating was reset.
    """
    if current_user and current_user.is_admin:
        try:
            # Validate the recipe_id
            validate_uuid(recipe_id)

            # Find the recipe in the database
            recipe = Recipe.find_one(id=recipe_id)

            if not recipe:
                return jsonify({'error': 'Recipe not found'}), 404

            # Reset user rating
            recipe.user_rating['count_positive'] = 0
            recipe.user_rating['count_negative'] = 0
            recipe.user_rating['score'] = 0

            # Commit the changes to the database
            db.session.merge(recipe)
            db.session.commit()

            # Return a success message
            return jsonify({'message': 'User rating reset successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Access denied. Admins only.'}), 403


@recipe_bp.route('/recipes/reset_all_ratings', methods=['POST'])
@jwt_required()
def reset_all_ratings():
    """
    Reset user rating for all recipes.

    Returns:
        JSON: A success message indicating that the ratings were reset.
    """
    if current_user and current_user.super_admin:
        try:
            # Fetch all recipes from the database
            recipes = Recipe.get_all()

            # Reset user ratings for all recipes
            for recipe in recipes:
                recipe.user_rating = {
                    'count_positive': 0,
                    'count_negative': 0,
                    'score': 0
                }

            # Commit the changes to the database
            db.session.commit()

            # Return a success message
            return jsonify({'message': 'User ratings reset for all recipes'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Access denied. Admins only.'}), 403