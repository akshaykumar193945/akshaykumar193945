from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class AdmissionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'))

class User_Credentials(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Define the one-to-many relationship between User_Credentials and AdmissionRecord
    # admission_records = db.relationship('AdmissionRecord', backref='user_credentials', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password  # You should hash the password before storing it
