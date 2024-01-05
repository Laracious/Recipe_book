from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, fullname, password):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


# curl -X POST -H "Content-Type: application/json" -d '{
#     "fullname": "wale Doe",
#     "username": "waleldoe",
#     "email": "waledoe@example.com",
#     "password": "@77w0rd"
# }' http://localhost:5000/register