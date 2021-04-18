
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
from .models import User, Question,QuestionCategory

views = Blueprint('views', __name__)

    
@views.route('/adminPage', methods=['GET', 'POST'])
@login_required
def adminPage():
    if current_user.auth=="admin":
        if request.method == 'POST':
            return render_template("adminPage.html", user= current_user)

        return render_template("adminPage.html", user= current_user)

    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user)

@views.route('/userManagment', methods=['GET', 'POST'])
@login_required
def userManagment():
    if current_user.auth=="admin":
        if request.method == 'POST':
            if request.form.get("addphide")=="1":
                print("add")
                user=User.query.filter_by(id = int(request.form.get("id_user"))).first()
                user.first_name=request.form.get("first_name")
                user.email=request.form.get("email")
                user.password=generate_password_hash( request.form.get("password"), method='sha256')
                user.auth=request.form.get("auth")
                db.session.add(user)
                db.session.commit()
                    
            elif request.form.get("deletephide")=="1":
                print("delete")
                user=User.query.filter_by(id = int(request.form.get("id_user"))).first()
                db.session.delete(user)
                db.session.commit()
            users=User.query.all()
            return render_template("userManagment.html", user= current_user,alluser=users)
        users = User.query.all()
        return render_template("userManagment.html", user= current_user ,alluser=users)
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


@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    if current_user.auth=="kid":
        if request.method == 'POST':
            list_dump=[]
            cat=request.form["cat"]
            if cat == "Animal":
                questions = Question.query.filter_by(cat = "Animal").all()
            elif cat== "Nature":
                questions = Question.query.filter_by(cat = "Nature").all()
            elif cat == "Math":
                questions = Question.query.filter_by(cat = "Math").all()  
            elif cat == "History":
                questions = Question.query.filter_by(cat = "History").all() 
            elif request.form["cat"] == "Color":
                questions = Question.query.filter_by(cat = "Color").all()
            questions=RandomQuestions(questions)
            for q in questions:
                list_dump.append(json.dumps(q,default=encoder_question))   
            session["questions"]=list_dump
            return redirect(url_for('views.question'))  
        cats = QuestionCategory.query.all()
        return render_template("kidPage.html", user=current_user, cats = cats)
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user)

def RandomQuestions(questions):
    for _ in range((len(questions)-1)//2):
        num_index=random.randint(1,len(questions)-1)
        temp=questions[0]
        questions[0]=questions[num_index]
        questions[num_index]=temp
        
    for j in range(len(questions)):
        for _ in range(2):
            num_answer=random.randint(1,3)
            if(num_answer==1):
                tempo=questions[j].answer4
                questions[j].answer4=questions[j].answer1
                questions[j].answer1=tempo
            elif(num_answer==2):
                tempo=questions[j].answer4
                questions[j].answer4=questions[j].answer2
                questions[j].answer2=tempo
            else:
                tempo=questions[j].answer4
                questions[j].answer4=questions[j].answer3
                questions[j].answer3=tempo    
    
    return questions

@views.route('/question',methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'POST':
        if request.form.get('finish1')=="1":        
            return redirect(url_for('views.kidPage'))
        if request.form['q_answer']==json.loads(session["questions"][0])['correct']:
            session["score"]+=50
            current_user.score=session["score"]
            db.session.commit() 
        else:
            return redirect(url_for('views.info'))
    
        session["questions"].pop(0)
        if len(session["questions"])!=0:
            question=json.loads(session["questions"][0])
            return render_template("question.html",user=current_user,  question = question,score=session["score"])
        else:
            return redirect(url_for('views.finishQuestions'))
    if current_user.auth=="kid":
        session["score"]=current_user.score
        question=json.loads(session["questions"][0])
        return render_template("question.html", user=current_user, question = question,score=session["score"])
    
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user)


def encoder_question(question):
    if isinstance(question,Question):
        return {'cat':question.cat,
        'question':question.question,
        'correct':question.correct,
        'answer1':question.answer1,
        'answer2':question.answer2,
        'answer3':question.answer3,
        'answer4':question.answer4,
        'url':question.url
        }
    raise TypeError(f'Object {question} is not type of Person.')  


@views.route('/info',methods=['GET', 'POST'])
@login_required    
def info():
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("info.html", user = current_user, question = json.loads(session["questions"][0]))

@views.route('/finishQuestions',methods=['GET', 'POST'])
@login_required    
def finishQuestions():
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("finishQuestions.html", user = current_user)

@views.route('/contentManagement')
def contentManagement():
    return render_template("contentManagement.html", user=current_user)

@views.route('/mailBox')
def mailBox():
    return render_template("mailBox.html", user=current_user)






