from flask import Flask, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from werkzeug.security import check_password_hash
from app.forms import RegistrationForm, LoginForm
from app import db

app = Flask(__name__)

# Route for favicon.ico
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# Single route for '/'
@app.route('/')
def dashboard():
    users = [
        {'id': 1, 'username': 'JohnDoe', 'email': 'john@example.com', 'role': 'Admin'},
        {'id': 2, 'username': 'JaneDoe', 'email': 'jane@example.com', 'role': 'User'}
    ]
    return render_template('dashboard.html', users=users)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        print(f'User added: {username}, {email}, {role}')
        return redirect(url_for('dashboard'))
    return render_template('add_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
