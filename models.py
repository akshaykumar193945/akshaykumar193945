from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

from datetime import datetime

class User_Credentials(db.Model, UserMixin):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)  # Adjust the length as needed
    email = db.Column(db.String(255), nullable=False)

    # Add a method to hash the password before saving
    # def set_password(self, password):
    #     self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class Profiles(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.username'), nullable=False)
    user = db.relationship('User_Credentials', backref=db.backref('profile', lazy=True))
