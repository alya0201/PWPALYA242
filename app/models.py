from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialize database
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False, default='user')  # Default role is user
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    # Set the password (Hashing it)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password (Comparing the hash)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Save method for adding new users to DB
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Update method for saving changes to an existing user
    def update(self):
        db.session.commit()

    # Delete method for removing a user
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # String representation
    def __repr__(self):
        return f"<User {self.username}, {self.email}, Role: {self.role}>"
    
    # Get user by email
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

