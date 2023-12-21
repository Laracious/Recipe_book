from flask_sqlalchemy import SQLAlchemy
import shortuuid
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from recipeapp import db

class BaseModel(db.Model):
    """BaseClass for all models"""

    # Make this class abstract so it won't be mapped to a database table
    __abstract__ = True

    # Define a primary key column with a default value of a generated UUID
    id = db.Column(
        db.String(22),
        primary_key=True, unique=True, nullable=False
        )
    createdAt = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False
        )
    updatedAt = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
        )

    def __init__(self, *args, **kwargs):
        """Initialize the class attributes"""
        super().__init__(*args, **kwargs)
        self.id = self.generate_id() if not self.id else self.id
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def generate_id(self):
        """Generate a unique short ID using shortuuid"""
        return shortuuid.uuid()

    def save(self):
        """Save the current object to the database"""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, **kwargs):
        """Create an instance of the model and save it to the database"""
        instance = cls(**kwargs)
        instance.save()
        return instance
    @classmethod
    def find_one(cls, **kwargs):
        """
        Finds the first row found in the table filtered by its arguments
        """
        try:
            return cls.query.filter_by(**kwargs).one()
        except NoResultFound:
            return None  # Return None if no row is found
        except MultipleResultsFound as e:
            # Handle the case where multiple rows are found (this should not happen for unique constraints)
            raise e
        finally:
            db.session.close()
    @classmethod
    def get_all(cls):
        """Get all users."""
        return cls.query.all()
    
    def update(self, **kwargs):
        """Update the current object with the provided key-value pairs"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updatedAt = datetime.now()
        db.session.commit()

    def delete(self):
        """Delete the current object from the database"""
        db.session.delete(self)
        db.session.commit()