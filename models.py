from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired

db = SQLAlchemy()

class AdmissionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)

# class AdmissionForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired()])
#     dob = StringField('Date of Birth', validators=[DataRequired()])
#     submit = SubmitField('Submit')
