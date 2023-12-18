from .recipe import Recipe
from .base_model import BaseModel, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel, UserMixin):
    """User model"""
    from .bookmarks import Bookmark
    __tablename__ = 'user'

    username = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Correct relationship definition with class name 'Recipe'
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    # Correct relationship definition with class name 'Recipe'
    bookmarks = db.relationship(
        'Recipe',
        secondary='bookmarks',
        lazy='subquery',
        backref=db.backref('bookmarked_by', lazy=True)
    )

    def __repr__(self):
        """Return a string representation of the User object"""
        return (
            f"Id: {self.id}, Username: {self.username}, "
            f"Name: {self.full_name}, Email: {self.email}"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username')
        self.full_name = kwargs.get('full_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.recipes = kwargs.get('recipes', [])
        self.bookmarks = kwargs.get('bookmarks', [])

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's hashed password"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert the recipe object to a dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    