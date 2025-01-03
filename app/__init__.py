from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User  # Pastikan model User Anda diimport

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Halaman login jika user tidak terautentikasi

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Ambil user dari database berdasarkan ID

    with app.app_context():
        from . import routes
        db.create_all()

    return app
