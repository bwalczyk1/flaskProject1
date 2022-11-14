from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    userName = StringField('Podaj swoję imię: ', validators=[DataRequired()])
    submit = SubmitField('Wyślij')

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'dfghj765$%^Kjhgd'


@app.route('/')
def index():
    userForm = NameForm()
    return render_template('weather.html', title='Strona główna', userForm=userForm)

@app.route('/user', methods=['POST'])
def user():
    userName = request.form['userName']
    return render_template('user.html', title='Użytkownik', userName=userName)

@app.route('/setSession', methods=['POSt', 'GET'])
def setSession():
    userForm = NameForm()
    if userForm.validate_on_submit():
        oldName = session.get('userName')
        if oldName is not None and oldName != userForm.userName.data:
            flash('Wygląda na to, że nazywasz się inaczej!')
        session['userName'] = userForm.userName.data
        return redirect(url_for('setSession'))
    return render_template('session.html', title="Zastosowanie sesji", userForm=userForm, userName=session.get('userName'))


# @app.route('user/name')
# def user(name):
#     return '<h1>Witaj, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run(debug=True)

