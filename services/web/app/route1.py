from flask import Flask,render_template,request,redirect,url_for,flash,session
#from build_app.chatbot_view import render_chatbot
from models import User
from sqlalchemy.exc import IntegrityError
#from bcrypt import hashpw, gensalt,checkpw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,current_user,login_required

#from db import User,UserDatabase
#import  auth


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
            email = request.form.get('email')
            password = request.form.get('password')
            user = User(email=email,password=generate_password_hash(password))
            if user:
                return redirect(url_for('index'))
            #hashed_password = generate_password_hash(password)
            #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            #user = User(name =name,email=email,password=hashed_password)
            #new_user = User(email=email,password=generate_password_hash(password))
            
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    
    @app.route('/login',methods = ['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                return redirect(url_for('index'))
            return "welcome sir"


    @app.route('/dashboard')
    #@auth.token_required("/", "admin")
    @login_required
    def dashboard():
        if current_user.is_authenticated:
            return dash_app.index()
        else:
            return "Unauthorized", 401