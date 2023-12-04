from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User_Credentials(db.Model, UserMixin):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Profiles(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.username'), nullable=False)
    user = db.relationship('User_Credentials', backref=db.backref('profile', lazy=True))
