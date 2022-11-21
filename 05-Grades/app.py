import json

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
date = datetime.now()
app.config['SECRET_KEY'] = 'dfghj765$%^Kjhgd'

class LoginForm(FlaskForm):
    userLogin = StringField('Nazwa użytkownika: ', validators=[DataRequired()])
    userPass = PasswordField('Hasło: ', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

users = {1: {'userLogin': 'lblitek', 'userPass': 'Qwerty123!', 'fname': 'Łukasz', 'lname': 'Blitek'}}

def countAverage(subjectValue, termValue):
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sumGrades = 0
    length = 0
    if subjectValue == "" and termValue == "":
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == "answer" or category == "quiz" or category == "test":
                        for grade in grades:
                            sumGrades += grade
                            length += 1
    elif termValue == "":
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    for category, grades in categories.items():
                        if category == "answer" or category == "quiz" or category == "test":
                            for grade in grades:
                                sumGrades += grade
                                length += 1
    else:
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    if term == termValue:
                        for category, grades in categories.items():
                            if category == "answer" or category == "quiz" or category == "test":
                                for grade in grades:
                                    sumGrades += grade
                                    length += 1
    return round(sumGrades/length, 2)

def getEndangered():
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectsString = ""
    for subject, terms in grades.items():
        if countAverage(subject, "") < 2:
            if subjectsString == "":
                subjectsString = subject
            else:
                subjectsString = subjectsString + ", " + subject
    if subjectsString == "":
        subjectsString = "brak zagrożeń"
    return subjectsString

def getHighest():
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectsArray = []
    for subject, terms in grades.items():
        avg = countAverage(subject, "")
        subjectsArray.append({"subject": subject, "average": avg})
    subjectsArray.sort(key=sortArray)
    while len(subjectsArray) > 2:
        subjectsArray.pop()
    return subjectsArray


def sortArray(k):
    return -k['average']

lstObj = [{'value' : -1},{'value' : 200},{'value' : 1},{'value' : 100},{'value' : 50}]



@app.route('/')
def index():
    return render_template('index.html', title='Strona główna')

@app.route('/login', methods=['POST', 'GET'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        userLogin = login.userLogin.data
        userPass = login.userPass.data
        if userLogin == users[1]['userLogin'] and userPass == users[1]['userPass']:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='Logowanie', login=login, userLogin=session.get('userLogin'))

@app.route('/logout')
def logout():
    session.pop('userLogin')
    return redirect('login  ')

@app.route('/dashboard')
def dashboard():
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'), date=date, grades=grades, categories=grades, countAverage=countAverage, getEndangered=getEndangered, getHighest=getHighest)

if __name__ == '__main__':
    app.run(debug=True)

