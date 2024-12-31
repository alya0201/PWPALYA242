from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Load environment variables
    load_dotenv()

    # Initialize Flask application
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///project.db')  # Defaults to SQLite
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Set a secret key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set the login view
    login_manager.login_view = 'login'

    # Import routes and models
    with app.app_context():
        from app import routes, models  # Ensures models and routes are loaded
    
    return app
