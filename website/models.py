from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    auth = db.Column(db.String(50))
    
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(150))
    question = db.Column(db.String(150))   
    correct = db.Column(db.String(150))
    wrong1 = db.Column(db.String(150))
    wrong2 = db.Column(db.String(150))
    wrong3 = db.Column(db.String(150))
