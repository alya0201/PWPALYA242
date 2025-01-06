from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app import db
from app.models import User
from .forms import RegistrationForm  # Hanya mengimpor RegistrationForm
from .forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')  # Pastikan file ini ada di folder templates

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('main.login'))

        # Create a new user
        user = User(username=username, email=email)
        user.set_password(password)  # Hash the password
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        current_app.logger.info(f"Attempting login for email: {email}")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            current_app.logger.info(f"Login successful for user_id: {user.id}")
            return redirect(url_for('main.dashboard'))  # Perbaikan indentasi
        else:
            current_app.logger.warning("Invalid login attempt")
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        current_app.logger.warning("Unauthorized access to dashboard")
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('main.login'))
    
    # Validasi pengguna dari database
    user = User.query.get(user_id)
    if not user:
        current_app.logger.warning(f"Invalid session detected for user_id: {user_id}")
        flash('Your session is invalid. Please login again.', 'danger')
        return redirect(url_for('main.login'))
    
    current_app.logger.info(f"Dashboard accessed by user_id: {user_id}")
    
    # Query data pengguna
    users = User.query.limit(100).all()  # Batasi hasil jika tabel besar
    return render_template('dashboard.html', users=users)

# Create User route
@main.route('/create', methods=['GET', 'POST'])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('create.html', form=form)

# Edit User route
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form.get('role', user.role)
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('User  updated successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit.html', user=user)

# Delete User route
@main.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User  deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))

# Logout route
@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))

if __name__ == '__main__':
    main.run(debug=True)