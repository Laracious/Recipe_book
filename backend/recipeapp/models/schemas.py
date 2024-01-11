from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """User Schema"""
    id = fields.String(dump_only=True)
    username = fields.String(
        required=True, validate=validate.Length(min=1, max=100)
    )
    full_name = fields.String(
        required=True, validate=validate.Length(min=1, max=100)
    )
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    is_admin = fields.Boolean()
    verified = fields.Boolean()
    #recipes = fields.List(fields.Nested('RecipeSchema', exclude=('user',)))
    #bookmarks = fields.List(fields.Nested('BookmarkSchema', exclude=('user_id',)))

class UserUpdateSchema(UserSchema):
    # Override the password field to make it optional
    password = fields.String(required=False)
class RecipeSchema(Schema):
    """Recipe Schema"""
    id = fields.String(dump_only=True)
    name = fields.String(
        required=True, validate=validate.Length(min=1, max=200)
    )
    description = fields.String()
    instructions = fields.String()
    user_id = fields.String(required=True)
    video = fields.String()
    user_rating = fields.Dict()
    ingredients = fields.Dict()
    image = fields.String()

class PaginationSchema(Schema):
    """Schema for pagination information"""
    page = fields.Integer()
    per_page = fields.Integer()
    total_items = fields.Integer()
    total_pages = fields.Integer()

class BookmarkSchema(Schema):
    """Bookmark Schema"""
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    recipe_id = fields.String(required=True)

class TokenBlocklistSchema(Schema):
    """
    Schema for the TokenBlocklist model.
    """
    id = fields.String(dump_only=True)
    jti = fields.String(required=True)
    expires_at = fields.DateTime(dump_only=True)