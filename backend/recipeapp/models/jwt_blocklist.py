from datetime import datetime, timedelta
from recipeapp.models.base_model import BaseModel
from recipeapp import db


class TokenBlocklist(BaseModel):
    """
    Model for storing revoked tokens in a blocklist.
    """
    jti = db.Column(db.String(36), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize a new TokenBlocklist instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        self.expires_at = self.createdAt + timedelta(hours=24)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check if a JTI exists in the blocklist and has not expired.

        Args:
            jti (str): JSON Web Token ID.

        Returns:
            bool: True if the JTI is blacklisted and has not expired,
            False otherwise.
        """
        return cls.query.filter_by(jti=jti).filter(
            cls.expires_at >= datetime.utcnow()).first() is not None