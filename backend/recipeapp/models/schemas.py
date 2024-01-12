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
class InstructionSchema(Schema):
    step1 = fields.Str()
    step2 = fields.Str()
    step3 = fields.Str()

class UserRatingSchema(Schema):
    count_negative = fields.Int()
    count_positive = fields.Int()
    score = fields.Float()

class RecipeSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    image = fields.Str()
    ingredients = fields.List(fields.Str(), allow_none=True)
    instructions = fields.Nested(InstructionSchema)
    user_rating = fields.Nested(UserRatingSchema)
    video = fields.Str()

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