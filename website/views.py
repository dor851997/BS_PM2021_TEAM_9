
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from . import db
import json
from .models import User, Question, QuestionCategory, MailBox ,Background,Score

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
            if request.form.get("editphide")=="1":##edit a user
                user=User.query.filter_by(id = int(request.form.get("editId"))).first()
                user.first_name=request.form.get("first_name")
                user.email=request.form.get("email")
                user.password=generate_password_hash( request.form.get("password"), method='sha256')
                user.auth=request.form.get("auth")
                db.session.add(user)
                db.session.commit()
                flash('Account edited!', category='success')
            elif request.form.get("addphide")=="1":
                AddUser()

            elif request.form.get("deletephide")=="1":##delete a user
                user=User.query.filter_by(id = int(request.form.get("deleteId"))).first()
                ref_score= Score.query.filter_by(user_id=user.id).first()
                db.session.delete(ref_score)
                db.session.commit()   
                db.session.delete(user)
                db.session.commit()
                flash('Account deleted!', category='success')
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


def AddUser():
    back=Background.query.all()
    email = request.form.get('add_email')
    first_name = request.form.get('add_firstname')
    password1 = request.form.get('add_password1')
    password2 = request.form.get('add_password2')
    auth = request.form.get('add_auth')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists.', category='error')
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    else:
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            password1, method='sha256'),auth=auth)
        db.session.add(new_user)
        db.session.commit()
        if(new_user.auth=="kid"):
            user = User.query.filter_by(email=email).first()
            new_score= Score(user_id=user.id)
            db.session.add(new_score)
            db.session.commit() 
        
        # login_user(new_user, remember=True)
        flash('Account created!', category='success')

    render_template("userManagment.html", user=current_user,background=back)


@views.route('/editorPage')
@login_required    
def editorPage():
    back=Background.query.all()
    if current_user.auth=="editor":
        return render_template("editorPage.html", user=current_user,background=back)
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
            session["category"] =cat
            if request.form["pick"]=="table":
                return redirect(url_for('views.score_table'))  
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
            quest=Question.query.filter_by(id=json.loads(session["questions"][0])['id']).first()
            quest.corrects+=1
            if session["category"]=="Animal":
                current_user.scores[0].animal_score=session["score"]
            elif session["category"]=="Nature":
                current_user.scores[0].nature_score=session["score"]
            elif session["category"]=="Math":
                current_user.scores[0].math_score=session["score"]
            elif session["category"]=="History":
                current_user.scores[0].history_score=session["score"]
            elif session["category"]=="Color":
                current_user.scores[0].color_score=session["score"]  
            db.session.commit()    
        else:
            quest=Question.query.filter_by(id=json.loads(session["questions"][0])['id']).first()
            quest.wrongs+=1
            db.session.commit()
            return redirect(url_for('views.info'))

        session["questions"].pop(0)
        if len(session["questions"])!=0:
            question=json.loads(session["questions"][0])
            return render_template("question.html",user=current_user,  question = question,score=session["score"],background=back)
        else:
            return redirect(url_for('views.finishQuestions'))
    if current_user.auth=="kid":
        if session["category"]=="Animal":
            session["score"]=current_user.scores[0].animal_score
        elif session["category"]=="Nature":
            session["score"]=current_user.scores[0].nature_score
        elif session["category"]=="Math":
            session["score"]=current_user.scores[0].math_score
        elif session["category"]=="History":
            session["score"]=current_user.scores[0].history_score
        elif session["category"]=="Color":
            session["score"]=current_user.scores[0].color_score
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
        return {'id':question.id,
        'cat':question.cat,
        'question':question.question,
        'correct':question.correct,
        'answer1':question.answer1,
        'answer2':question.answer2,
        'answer3':question.answer3,
        'answer4':question.answer4,
        'timer':question.timer,
        'url':question.url,
        'corrects':question.corrects,
        'wrongs':question.wrongs,
        'photoUrl':question.photoUrl
        }
    raise TypeError(f'Object {question} is not type of Person.')  

@views.route('/score-table',methods=['GET', 'POST'])
@login_required   
def score_table():
    back=Background.query.all()
    users=User.query.filter_by(auth="kid").all()
    users=SortByScore(users)
    scores=getScores(users)
    return render_template("score_table.html", user=current_user,background=back,users=users,n=len(users),scores=scores)

def getScores(users):
    scores=[]
    if session["category"]=="Animal":
        for i in range(len(users)):
            scores.append(users[i].scores[0].animal_score)
    elif session["category"]=="Nature":
        for i in range(len(users)):
            scores.append(users[i].scores[0].nature_score)
    elif session["category"]=="Math":
        for i in range(len(users)):
            scores.append(users[i].scores[0].math_score)
    elif session["category"]=="History":
        for i in range(len(users)):
            scores.append(users[i].scores[0].history_score)
    elif session["category"]=="Color":
        for i in range(len(users)):
            scores.append(users[i].scores[0].color_score)
    return scores

def SortByScore(users):
    tempusers = []
    for i in range(len(users)):
        tempusers.insert(i,users[i])
    for i in range(len(tempusers)):
        k=i+1
        for j in range(k,len(tempusers)):
            getScoreCategory(us=tempusers[i])
            if getScoreCategory(us=tempusers[i])<getScoreCategory(us=tempusers[j]):
                temp=tempusers[i]
                tempusers[i]=tempusers[j]
                tempusers[j]=temp
    return tempusers

def getScoreCategory(us):
    if session["category"]=="Animal":
        return us.scores[0].animal_score
    elif session["category"]=="Nature":
        return us.scores[0].nature_score
    elif session["category"]=="Math":
        return us.scores[0].math_score
    elif session["category"]=="History":
        return us.scores[0].history_score
    elif session["category"]=="Color":
        return us.scores[0].color_score
   
        
 
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
@login_required 
def contentManagement():
    back=Background.query.all()
    cat=QuestionCategory.query.all()
    if request.method == 'POST':
        if request.form.get("addphide")=="1":
            cate = request.form.get('category')
            que = request.form.get('question')
            correct_ans = request.form.get('correct_ans')
            answer1 = request.form.get('answer1')
            answer2 = request.form.get('answer2')
            answer3 = request.form.get('answer3')
            answer4 = request.form.get('answer4')
            url = request.form.get('url')
            photoUrl = request.form.get('photoUrl')
            question = Question(cat = cate, question = que, correct = correct_ans, answer1 = answer1, answer2 = answer2, answer3 = answer3, answer4 = answer4, url = url ,photoUrl=photoUrl)
            db.session.add(question)
            db.session.commit()
        elif request.form.get("editphide")=="1":
            question=Question.query.filter_by(id = int(request.form.get("editId"))).first()
            question.cat=request.form.get('category')
            question.question=request.form.get('question')
            question.correct=request.form.get('correct_ans')
            question.answer1=request.form.get('answer1')
            question.answer2=request.form.get('answer2')
            question.answer3=request.form.get('answer3')
            question.answer4=request.form.get('answer4')
            question.timer=request.form.get('timer')
            question.url=request.form.get('url')
            question.photoUrl=request.form.get('photoUrl')
            db.session.add(question)
            db.session.commit()
        elif request.form.get("deletephide")=="1":
            question=Question.query.filter_by(id = int(request.form.get("deleteId"))).first()
            db.session.delete(question)
            db.session.commit()
    questions = Question.query.all()
    return render_template("contentManagement.html", user=current_user, questions = questions,background=back,category=cat)

@views.route('/mailBox',methods=['GET', 'POST'])
@login_required 
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
@login_required 
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
@login_required 
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


@views.route('/update-background', methods=['POST'])
@login_required 
def update_background():
    
    data = json.loads(request.data)
    backId = data['backId']
    back = Background.query.get(backId)
    current_user.background=back.picture
    db.session.commit()
    return jsonify({})

@views.route('/tableManagment', methods=['GET', 'POST'])
@login_required
def tableManagment():
    if request.method == 'POST':
        if request.form.get("editphide")=="1":##edit a score
            user=User.query.filter_by(id = int(request.form.get("editId"))).first()
            score = Score.query.filter_by(user_id = user.id).first()
            if request.form.get("cat") == "Animal":
                score.animal_score = request.form.get("auth")
            elif request.form.get("cat") == "Nature":
                score.nature_score = request.form.get("auth")
            elif request.form.get("cat") == "Math":
                score.math_score = request.form.get("auth")
            elif request.form.get("cat") == "History":
                score.history_score = request.form.get("auth")
            elif request.form.get("cat") == "Color":
                score.color_score = request.form.get("auth")
            print(user.first_name)
            print(score.id)
            db.session.add(score)
            db.session.commit()
            flash('Account edited!', category='success')
    back=Background.query.all()
    users=User.query.filter_by(auth="kid").all()
    session["category"] = "Animal"
    animal_cat = "Animal"
    animal_users=SortByScore(users)
    animal_scores=getScores(animal_users)
    session["category"] = "Nature"
    nature_cat = "Nature"
    nature_users=SortByScore(users)
    nature_scores=getScores(nature_users)
    session["category"] = "Math"
    math_cat = "Math"
    math_users=SortByScore(users)
    math_scores=getScores(math_users)
    session["category"] = "History"
    history_cat = "History"
    history_users=SortByScore(users)
    history_scores=getScores(history_users)
    session["category"] = "Color"
    color_cat = "Color"
    color_users=SortByScore(users)
    color_scores=getScores(color_users)
    return render_template("tableManagment.html", user=current_user, background=back, animal_users=animal_users, animal_scores=animal_scores, 
    nature_users=nature_users, nature_scores=nature_scores, math_users=math_users, math_scores=math_scores, history_users=history_users, history_scores=history_scores,
     color_users=color_users, color_scores=color_scores, animal_cat=animal_cat, nature_cat=nature_cat, math_cat=math_cat, history_cat=history_cat,
     color_cat=color_cat,a=len(animal_users), n=len(nature_users), m=len(math_users), h=len(history_users), c=len(color_users))

    

@views.route('/questionsReport', methods=['GET', 'POST'])
@login_required 
def questionsReport():
    back=Background.query.all()
    questions=Question.query.all()
    category=QuestionCategory.query.all()
    return render_template("questionsReport.html",user=current_user,questions=questions,background=back,category=category) 

@views.route('/hallOfFame', methods=['GET', 'POST'])
@login_required
def hallOfFame():
    back=Background.query.all()
    users=User.query.filter_by(auth="kid").all()
    session["category"] = "Animal"
    animal_cat = "Animal"
    animal_users=SortByScore(users)
    animal_scores=getScores(animal_users)
    session["category"] = "Nature"
    nature_cat = "Nature"
    nature_users=SortByScore(users)
    nature_scores=getScores(nature_users)
    session["category"] = "Math"
    math_cat = "Math"
    math_users=SortByScore(users)
    math_scores=getScores(math_users)
    session["category"] = "History"
    history_cat = "History"
    history_users=SortByScore(users)
    history_scores=getScores(history_users)
    session["category"] = "Color"
    color_cat = "Color"
    color_users=SortByScore(users)
    color_scores=getScores(color_users)
    return render_template("hallOfFame.html",user=current_user, background=back, animal_user=animal_users[0], animal_score=animal_scores[0], 
    nature_user=nature_users[0], nature_score=nature_scores[0], math_user=math_users[0], math_score=math_scores[0], history_user=history_users[0], history_score=history_scores[0],
     color_user=color_users[0], color_score=color_scores[0], animal_cat=animal_cat, nature_cat=nature_cat, math_cat=math_cat, history_cat=history_cat,
     color_cat=color_cat)