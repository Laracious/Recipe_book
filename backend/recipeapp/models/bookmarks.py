from .base_model import BaseModel, db


class Bookmark(BaseModel):
    """Bookmark model"""

    __tablename__ = 'bookmarks'

    user_id = db.Column(
        db.String(22), db.ForeignKey('user.id'), nullable=False
    )
    recipe_id = db.Column(
        db.String(22), db.ForeignKey('recipe.id'), nullable=False
    )