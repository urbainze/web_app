from flask import Flask,render_template,request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from build_apps.create_app import create_dash_app 
from flask_login import UserMixin
from flask import Flask,render_template,request,redirect,url_for,flash,session
#from build_app.chatbot_view import render_chatbot
#from models import User
from sqlalchemy.exc import IntegrityError
#from bcrypt import hashpw, gensalt,checkpw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,current_user,login_required


#db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mydb.db'

    app.secret_key = 'wxyzabc'
    db = SQLAlchemy(app)
    migrate = Migrate(app,db)
    #db.init_app(app)
    #bcrypt = Bcrypt(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    dash_app = create_dash_app(app)

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    class User(db.Model,UserMixin):
       __tablename__ = 'users'

       uid = db.Column(db.Integer,primary_key=True)
       email = db.Column(db.String(80),unique=True,nullable=False)
       #name = db.Column(db.String(80),nullable=False)
       password = db.Column(db.String(256),nullable=False)
       is_admin = db.Column(db.Boolean,default=True)

    def get_uid(self):
        return self.uid

    def get_email(self):
        return self.email
    
    #bcrypt = Bcrypt(app)

    #from route1 import register_routes

    #register_routes(app,db,dash_app,bcrypt)
    #register_routes(app,db,dash_app)

    #migrate = Migrate(app,db)
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

    return app




