
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
from .models import User, Question, QuestionCategory, MailBox ,Background

views = Blueprint('views', __name__)

    
@views.route('/adminPage', methods=['GET', 'POST'])
@login_required
def adminPage():
    back=Background.query.all()
    if current_user.auth=="admin":
        if request.method == 'POST':
            return render_template("adminPage.html", user= current_user)

        return render_template("adminPage.html", user= current_user,background=back)

    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user,background=back)

@views.route('/userManagment', methods=['GET', 'POST'])
@login_required
def userManagment():
    back=Background.query.all()
    if current_user.auth=="admin":
        if request.method == 'POST':
            if request.form.get("addphide")=="1":##edit a user
                user=User.query.filter_by(id = int(request.form.get("id_user"))).first()
                user.first_name=request.form.get("first_name")
                user.email=request.form.get("email")
                user.password=generate_password_hash( request.form.get("password"), method='sha256')
                user.auth=request.form.get("auth")
                db.session.add(user)
                db.session.commit()
            elif request.form.get("deletephide")=="1":##delete a user
                user=User.query.filter_by(id = int(request.form.get("id_user"))).first()
                db.session.delete(user)
                db.session.commit()
            users=User.query.all()
            return render_template("userManagment.html", user= current_user,alluser=users,background=back)
        users = User.query.all()
        return render_template("userManagment.html", user= current_user ,alluser=users,background=back)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user,background=back)
    
@views.route('/editorPage')
@login_required    
def editorPage():
    back=Background.query.all()
    if current_user.auth=="editor":
        return render_template("editorPage.html", user=current_user)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("kidPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter editor page.", category='error')
        return render_template("adminPage.html", user=current_user,background=back)


@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    back=Background.query.all()
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
        return render_template("kidPage.html", user=current_user, cats = cats,background=back)
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user,background=back)

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
    back=Background.query.all()
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
            return render_template("question.html",user=current_user,  question = question,score=session["score"],background=back)
        else:
            return redirect(url_for('views.finishQuestions'))
    if current_user.auth=="kid":
        session["score"]=current_user.score
        question=json.loads(session["questions"][0])
        return render_template("question.html", user=current_user, question = question,score=session["score"],background=back)
    
    elif current_user.auth=="editor":
        flash("No Permission to current user to enter kid page.", category='error')
        return render_template("editorPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("adminPage.html", user=current_user,background=back)


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
    back=Background.query.all()
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("info.html", user = current_user, question = json.loads(session["questions"][0]),background=back)

@views.route('/finishQuestions',methods=['GET', 'POST'])
@login_required    
def finishQuestions():
    back=Background.query.all()
    if request.method == 'POST':
        return redirect(url_for('views.kidPage'))
    if current_user.auth=="kid":
        return render_template("finishQuestions.html", user = current_user,background=back)

@views.route('/contentManagement', methods=['GET', 'POST'])
def contentManagement():
    back=Background.query.all()
    if request.method == 'POST':
        if request.form.get("addphide")=="1":
            print("add")
            cat = request.form.get('category')
            que = request.form.get('question')
            correct_ans = request.form.get('correct_ans')
            answer1 = request.form.get('answer1')
            answer2 = request.form.get('answer2')
            answer3 = request.form.get('answer3')
            answer4 = request.form.get('answer4')
            url = request.form.get('url')
            question = Question(cat = cat, question = que, correct = correct_ans, answer1 = answer1, answer2 = answer2, answer3 = answer3, answer4 = answer4, url = url)
            db.session.add(question)
            db.session.commit()
        elif request.form.get("deletephide")=="1":
            print("delete")
            question=Question.query.filter_by(id = int(request.form.get("id_question"))).first()
            db.session.delete(question)
            db.session.commit()
    questions = Question.query.all()
    return render_template("contentManagement.html", user=current_user, questions = questions,background=back)

@views.route('/mailBox',methods=['GET', 'POST'])
def mailBox():
    back=Background.query.all()
    mail = MailBox.query.filter_by(to = str(current_user.email))
    if request.method == 'POST':
        to = request.form.get('to')
        From = current_user.email
        subject = request.form.get('subject')
        message = request.form.get('message')
        new_mail = MailBox(From = From, to = to, message = message, subject = subject)
        db.session.add(new_mail)
        db.session.commit()
        return render_template("mailBox.html", user=current_user, mails=mail,background=back)
    return render_template("mailBox.html", user=current_user, mails=mail,background=back)

@views.route('/mailBoxEditor', methods=['GET', 'POST'])
def mailBoxEditor():
    back=Background.query.all()
    mail = MailBox.query.filter_by(to = str(current_user.email))
    if request.method == 'POST':
        to = request.form.get('to')
        From = current_user.email
        subject = request.form.get('subject')
        message = request.form.get('message')
        new_mail = MailBox(From = From, to = to, message = message, subject = subject)
        db.session.add(new_mail)
        db.session.commit()
        return render_template("mailBoxEditor.html", user=current_user, mails=mail,background=back)
    return render_template("mailBoxEditor.html", user=current_user, mails=mail,background=back)

@views.route('/selectBackgrounds', methods=['GET', 'POST'])
def selectBackgrounds():
    back=Background.query.all()
    if current_user.auth=="admin":
        if request.method == 'POST':
            print(request.form.getlist("check"))
            for b in back:
                if b.name in request.form.getlist("check"):
                    b.checked="true"
                else:
                    b.checked="false"
            db.session.commit()
            back=Background.query.all()
        return render_template("selectBackgrounds.html", user=current_user ,background=back)
    elif current_user.auth=="kid":
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("kidPage.html", user=current_user,background=back)
    else:
        flash("No Permission to current user to enter admin page.", category='error')
        return render_template("editorPage.html", user=current_user,background=back)



