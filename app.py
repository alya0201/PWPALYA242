# In app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('instance', 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate =Migrate(app, db)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists!', 'danger')
            return redirect(url_for('register'))

        # Hash password and save user to database
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, role=role, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, role=role, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']
        user.email = request.form['email']
        
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'], method='sha256')

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
