from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User  # Assuming User model is in models.py
from werkzeug.security import check_password_hash
from flask_login import LoginManager
from app.forms import RegistrationForm, LoginForm  # Assuming forms.py for handling forms


# Home Route
@app.route('/')
def home():
    return render_template('dashboard.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the user already exists
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash('An account with that email already exists!', 'danger')
            return redirect(url_for('login'))
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user.save()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check your email and password.', 'danger')
    
    return render_template('login.html', form=form)


# Dashboard Route (Login Required)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'info')
    return redirect(url_for('home'))
