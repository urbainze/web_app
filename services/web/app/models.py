from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()
login_manager = LoginManager()



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.uid)

    def get_email(self):
        return self.email
    
    def db_app(app):
        db = SQLAlchemy(app)