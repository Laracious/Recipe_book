from .recipe import Recipe
from .base_model import BaseModel, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity

class User(BaseModel, UserMixin):
    """User model"""
    from .bookmarks import Bookmark
    __tablename__ = 'user'

    username = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    otp = db.Column(db.Integer, nullable=True)

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
            f"Is Admin: {self.is_admin}"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username')
        self.full_name = kwargs.get('full_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.is_admin = kwargs.get('is_admin', False)
        self.recipes = kwargs.get('recipes', [])
        self.otp = kwargs.get('otp')
        self.bookmarks = kwargs.get('bookmarks', [])
        
        #Hash the password in the initialization
        password = kwargs.get('password')
        if password:
            self.password = generate_password_hash(password)
    def check_password(self, password):
        """Check if the provided password matches the user's hashed password"""
        return check_password_hash(self.password, password)
    
    @classmethod
    def find_one_with_relationships(cls, **kwargs):
        return cls.query.options(
            db.joinedload(cls.recipes), db.joinedload(cls.bookmarks)
            ).filter_by(**kwargs).one_or_none()

    def format(self):
        """Convert the recipe object to a dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "is_admin": self.is_admin,
            # "createdAt": self.createdAt,
            # "updatedAt": self.updatedAt
        }
    