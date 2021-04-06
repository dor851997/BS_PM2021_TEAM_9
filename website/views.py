
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,session
from flask_login import login_required, current_user

from . import db
import json
from .models import User, Question,QuestionCategory

views = Blueprint('views', __name__)

@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    if current_user.auth=="kid":
        if request.method == 'POST':
            if request.form['submit_button'] == 'Start a quiz!':
                return redirect(url_for('views.question'))
        cats = QuestionCategory.query.all()
        return render_template("kidPage.html", user=cats)
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user)
    

@views.route('/adminPage', methods=['GET', 'POST'])
@login_required
def adminPage():
    if current_user.auth=="admin":
        return render_template("adminPage.html", user=current_user)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user)
    
@views.route('/editorPage')
@login_required    
def editorPage():
    if current_user.auth=="editor":
        return render_template("editorPage.html", user=current_user)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("kidPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("adminPage.html", user=current_user)
   

score=0
@views.route('/question',methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'POST':
        if request.form['q_answer']==json.loads(session["questions"][0])['correct']:
            session["score"]=session["score"]+50
            current_user.score = current_user.score + 50
            db.session.commit()
        else:
            return redirect(url_for('views.kidPage'))

        session["questions"].pop(0)
        if len(session["questions"])!=0:
            question=json.loads(session["questions"][0])
            return render_template("question.html", user=question,score=session["score"])
    
    if current_user.auth=="kid":
        questions = Question.query.filter_by(cat = "Animal").all()
        list=[]
        for q in questions:
            list.append(json.dumps(q,default=encoder_question))   
        session["questions"]=list
        session["score"]=0
        question=json.loads(session["questions"][0])
        return render_template("question.html", user=question,score=session["score"])
    
    
    return render_template("question.html", user=current_user,score=score)



def encoder_question(question):
    if isinstance(question,Question):
        return {'cat':question.cat,
        'question':question.question,
        'correct':question.correct,
        'wrong1':question.wrong1,
        'wrong2':question.wrong2,
        'wrong3':question.wrong3
        }
    raise TypeError(f'Object {question} is not type of Person.')  
