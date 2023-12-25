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

    @classmethod
    def find_bookmarks_by_user(cls, user_id):
        """Find all bookmarks for a user"""
        return cls.query.filter_by(user_id=user_id).all()

    def create_or_delete_bookmark(self):
        """Create or delete a bookmark based on its existence"""
        existing_bookmark = self.find_one(
            user_id=self.user_id,
            recipe_id=self.recipe_id
            )

        if existing_bookmark:
            # If bookmark exists, delete it
            existing_bookmark.delete()
            return "Bookmark deleted successfully"
        else:
            # If bookmark doesn't exist, create it
            self.save()
            return "Bookmark created successfully"
