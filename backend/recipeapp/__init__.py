from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, jsonify
from sqlalchemy.exc import OperationalError
from .config import Config
from flasgger import Swagger
from flask_caching import Cache
import yaml
import os
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler

# Initialize SQLAlchemy
db = SQLAlchemy()

# Create an instance of the APScheduler
scheduler = APScheduler()

# Create an instance of Swagger
swagger = Swagger()

#Create an instance of the cach
cache = Cache()


mail = Mail()  # Create the mail object

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    #app.config.from_object(Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print("using db")


    # Initialize CORS
    CORS(app, supports_credentials=True)

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(e):
        return jsonify(
            {"error": "Database connection error", "message": str(e)}
            ), 500


    # Load Swagger content from the file
    with open("swagger_config.yaml", "r") as file:
        swagger_config = yaml.load(file, Loader=yaml.FullLoader)
    # Initialize Flasgger with the loaded Swagger configuration
    Swagger(app, template=swagger_config)

    #initialize the caching system
    cache.init_app(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Secret key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com' #'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465 # 587
    app.config['MAIL_USE_SSL'] = True # False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'muazuidrisyakub@yahoo.com'

    # JWT
    app.config['ACCESS_SECRET_KEY'] = os.getenv('ACCESS_SECRET_KEY')
    app.config['REFRESH_SECRET_KEY'] = os.getenv('REFRESH_SECRET_KEY')

    # Set the JWT_SECRET_KEY in the app configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    jwt = JWTManager(app)  # Instantiate the JWTManager class
    jwt.init_app(app)  # initialize the JWTManager with your app
    
    # Initialize the scheduler
    scheduler.init_app(app)
    scheduler.start()
        
    #jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'message': 'The token has expired',
            'error': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token is not fresh',
            'error': 'fresh_token_required'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token has been revoked',
            'error': 'token_revoked'
        }), 401
    
    
    from recipeapp.models.user import User
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == "imuaz":
            user = User.query.filter_by(username=identity).first()
            if user:
                user.is_admin = True
                db.session.commit()
        return None
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email=identity).one_or_none()
    
    # Callback function to check if a JWT exists in the blocklist
    from recipeapp.models.jwt_blocklist import TokenBlocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlocklist.is_jti_blacklisted(jti)
    
    # @jwt.user_claims_loader
    # def add_claims_to_user(user):
    #     return {'is_admin': user.is_admin}
    
    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     return user.id
    
    

    # # Initialize Flask-Mail
    mail.init_app(app)  # Initialize Flask-Mail with your app

    # imports blueprints
    from recipeapp.routes.users import user_bp
    from recipeapp.routes.recipes import recipe_bp
    from recipeapp.routes.bookmark import bookmark_bp

    # register blueprint
    app.register_blueprint(user_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(bookmark_bp)

    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app