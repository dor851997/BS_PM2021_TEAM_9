
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from . import db
import json
from .models import User, Question,QuestionCategory

views = Blueprint('views', __name__)

@views.route('/kidPage', methods=['GET', 'POST'])
@login_required
def kidPage():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Start a quiz!':
            return redirect(url_for('views.question'))
    cats = QuestionCategory.query.all()
    return render_template("kidPage.html", user=cats)
    

@views.route('/adminPage', methods=['GET', 'POST'])
@login_required
def adminPage():
    
    return render_template("adminPage.html", user=current_user)

@views.route('/userManagment', methods=['GET', 'POST'])
@login_required
def userManagment():
   
    return render_template("userManagment.html", user=current_user)

@views.route('/editorPage')
@login_required    
def editorPage():
    
    return render_template("editorPage.html", user=current_user)
   

@views.route('/question')
@login_required
def question():
    # question = Question.query.all()
    cat = Question.query.filter_by(cat = "Animal").first()
    print(cat.cat)
    if current_user.auth=="kid":
        return render_template("question.html", user=cat)
        
    return render_template("question.html", user=current_user)