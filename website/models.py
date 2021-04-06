from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    auth = db.Column(db.String(50))
    score = db.Column(db.Integer)
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(150))
    question = db.Column(db.String(150))   
    correct = db.Column(db.String(150))
    wrong1 = db.Column(db.String(150))
    wrong2 = db.Column(db.String(150))
    wrong3 = db.Column(db.String(150))
    url = db.Column(db.String(1500))

class QuestionCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(150))
    picture=db.Column(db.String(150))

class BestScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserID= db.Column(db.Integer, unique=True)
    score= db.Column(db.Integer)
    cat = db.Column(db.String(150))
    