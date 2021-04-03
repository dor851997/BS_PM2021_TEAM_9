
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from . import db
import json
from .models import User, Question,QuestionCategory

views = Blueprint('views', __name__)

@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    # users=User.query.all()
    # us=User.query.filter_by(email='asdad@gmail.com').first()
    # print(us.email)
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

@views.route('/adminPage')
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

@views.route('/question')
@login_required
def question():
    # question = Question.query.all()
    cat = Question.query.filter_by(cat = "Animal").first()
    print(cat.cat)
    if current_user.auth=="kid":
        return render_template("question.html", user=cat)
        
    return render_template("question.html", user=current_user)