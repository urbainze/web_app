from flask import Flask,render_template,request,redirect,url_for,flash,session
#from build_app.chatbot_view import render_chatbot
from models import User
from sqlalchemy.exc import IntegrityError
#from bcrypt import hashpw, gensalt,checkpw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,current_user,login_required

from db import User,UserDatabase
import  auth


#def register_routes(app,db,dash_app,bcrypt):
def register_routes(app,db,dash_app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/signup',methods = ['GET','POST'])
    def signup():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            #name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            #hashed_password = generate_password_hash(password)
            #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            #user = User(name =name,email=email,password=hashed_password)
            #user = User(name =name,email=email,password=hashed_password)
            
            db_user = UserDatabase()
            db_user.create_user(email, password)
            del db_user
            return redirect(url_for('index'))
            '''try:
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created!', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                # Handle the case where the email is already unique
                db.session.rollback()
                flash('Email already exists. Please choose a different one.', 'error')
                return render_template('register.html')
            finally:
                   # Close the session even if an exception occurs
                db.session.close()'''
    
    @app.route('/login',methods = ['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            valid = auth.check_credentials(email, password)
            print(valid)
            #user = User.query.filter_by(email=email).first()
            '''#if bcrypt.check_password_hash(user.password,password):
            if user and check_password_hash(user.password, password):
                if current_user.is_admin == True :
                    login_user(user)
                    session['email'] = email
                    flash('Welcome User!', 'success')
                    #return redirect(url_for('dashboard'))
                    return "welcome admin"
                else:
                    login_user(user)
                    session['email'] = email
                    flash('Welcome User!', 'success')
                    return "welcome simple user "

            else:
                # Handle unsuccessful login (display error message, etc.)
                flash('Login unsuccessful. Please check your username and password.', 'danger')
                error_message = "Invalid email or password."
                return render_template('login.html', error=error_message)
                '''
            if  not valid:
                #login_user(user)
                #session['email'] = email
                #flash('Welcome User!', 'success')
                return "welcome sir"
            else:
                #flash('Login unsuccessful. Please check your username and password.', 'danger')
                error_message = "Invalid email or password."
                return render_template('index.html', error=error_message)


    @app.route('/dashboard')
    #@auth.token_required("/", "admin")
    @login_required
    def dashboard():
        if current_user.is_authenticated:
            return dash_app.index()
        else:
            return "Unauthorized", 401