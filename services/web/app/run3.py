
from flask import Flask, render_template, request, redirect, url_for, flash, session,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask import current_app
from build_apps.create_app import create_dash_app1
from build_apps import admin_page
import db1
from db1 import User,UserDatabase
from auth1 import check_credentials

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.secret_key = 'wxyzabc'


db = UserDatabase()

login_manager = LoginManager()
login_manager.init_app(app)





dash_app1  = create_dash_app1(app,name='dash1')


@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    #user = User(user_id=email, password=password)
    db.create_user(user_id=email, password=password)  
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User(user_id=email, password=password)
    if check_credentials(user_id=email, password=password):
        #login_user(user)
        session['email'] = email
        session['role'] = user.role
        return redirect(url_for('dashboard1'))
    flash('Invalid email or password', 'error')
    return redirect(url_for('index'))


@app.route('/dashboard1')
def dashboard1():
    return dash_app1.index()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the session data
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


#if __name__ == "__main__":
    #app.run(host = '0.0.0.0',debug=True, port=8057)