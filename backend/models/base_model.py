from flask_sqlalchemy import SQLAlchemy
import shortuuid
from datetime import datetime

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

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()

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
