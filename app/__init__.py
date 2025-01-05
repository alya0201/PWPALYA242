import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate


# Inisialisasi objek
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Ganti dengan kunci rahasia Anda
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Ganti dengan URI database Anda

    # Inisialisasi objek dengan aplikasi
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Konfigurasi Logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    app.logger.setLevel(logging.INFO)

    # Contoh log saat aplikasi dibuat
    app.logger.info("Aplikasi Flask berhasil diinisialisasi.")

    # Definisikan user_loader
    @login_manager.user_loader
    def load_user(user_id):
        # Logika untuk memuat pengguna dari database
        return None  # Ganti dengan logika pemuatan pengguna yang sesuai
    
    # Import dan registrasi blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
