from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    auth = db.Column(db.String(50))
    scores = db.relationship('Score')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_score=db.Column(db.Integer,default=0)
    nature_score=db.Column(db.Integer,default=0)
    math_score=db.Column(db.Integer,default=0)
    history_score=db.Column(db.Integer,default=0)
    color_score=db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Background(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(150))
    name = db.Column(db.String(150))
    checked= db.Column(db.String(150))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(150))
    question = db.Column(db.String(150))   
    correct = db.Column(db.String(150))
    answer1 = db.Column(db.String(150))
    answer2 = db.Column(db.String(150))
    answer3 = db.Column(db.String(150))
    answer4 = db.Column(db.String(150))
    url = db.Column(db.String(1500))

class QuestionCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(150))
    picture=db.Column(db.String(150))


    
class MailBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    From = db.Column(db.String(150))
    to = db.Column(db.String(150))
    message = db.Column(db.String(1000))
    subject = db.Column(db.String(150))


