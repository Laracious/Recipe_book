import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '2887b795db634c52e3a9e7656bb3d56e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)

db = SQLAlchemy(app)

# Import models and routes
from .routes import recipes, users
from .models import bookmarks, recipe, base_model, user

# Create tables if they do not exist
with app.app_context():
    db.create_all()