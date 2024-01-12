from marshmallow import ValidationError
import shortuuid
import re

def validate_uuid(value):
    """
    A custom validator function that checks if a value is a valid shortuuid.
    """
    if len(value) != 22:
        raise ValidationError("Invalid uuid length.")

    try:
        # Try to decode the provided value as a shortuuid
        shortuuid.decode(value)
    except ValueError:
        # If decoding fails, raise a validation error
        raise ValidationError("Invalid uuid.")
    
def validate_psswd(password):
    """
    Validate the password based on the specified criteria:
    - Minimum 8 characters
    - At least 1 lowercase character
    - At least 1 uppercase character
    - At least 1 digit
    - At least 1 special character (!@#$%^&*()-_+=<>?/{},.)
    """
    if (
        len(password) < 8 or
        not any(char.islower() for char in password) or
        not any(char.isupper() for char in password) or
        not any(char.isdigit() for char in password) or
        not any(char in r'!@#$%^&*()-_+=<>?/{},.' for char in password)
    ):
        raise ValueError("Invalid password format")

def validate_email(email):
    """
    Validate the email format using a regular expression.
    """
    email_pattern = re.compile(
        r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    )
    if not email_pattern.match(email):
        raise ValueError("Invalid email format")

def validate_username(username):
    """
    Validate the username format using a regular expression.
    Allow only characters, underscores, and digits.
    """
    username_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    if not username_pattern.match(username):
        raise ValueError("Invalid username format")
