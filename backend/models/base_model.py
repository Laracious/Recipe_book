from flask_sqlalchemy import SQLAlchemy
import shortuuid
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError, NoResultFound

db = SQLAlchemy()

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
            instance = cls.query.filter_by(**kwargs).one()
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e
        finally:
            db.session.close()
        return instance

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

    @classmethod
    def find_user_by(cls, **kwargs):
        """
        Finds the first row found in the users table filtered by its arguments
        """
        return cls.find_one(**kwargs)

    @classmethod
    def update_user(cls, user_id: int, **kwargs) -> None:
        """
        Update the user’s attributes as passed in its arguments
        """
        user = cls.find_one(id=user_id)
        user.update(**kwargs)