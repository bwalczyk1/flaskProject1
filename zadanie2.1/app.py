from flask import Flask, render_template, request
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'dfghj765$%^Kjhgd'

class NumbersForm(FlaskForm):
    numbers = StringField('Podaj ciąg liczb oddzielonych przecinkami: ', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


@app.route('/', methods=["POST", "GET"])
def index():
    numbersForm = NumbersForm()
    if request.method == "GET":
        return render_template('weather.html', title='Zadanie 2.1', numbersForm=numbersForm)

    numbersString = request.form['numbers']
    numbers = [int(numStr) for numStr in numbersString.split(",")]
    numbers.sort(reverse=True)
    maxNumber = 'Wartość maksymalna: ' + str(max(numbers))
    minNumber = 'Wartość minimalna: ' + str(min(numbers))
    avgNumber = 'Średnia ciągu: ' + str(sum(numbers)/len(numbers))
    sortedNumbers = 'Posortowany malejąco ciąg: ' + ','.join(str(n) for n in numbers)
    return render_template('weather.html', title='Zadanie 2.1', numbersForm=numbersForm, data=[sortedNumbers, minNumber, maxNumber, avgNumber])

if __name__ == '__main__':
    app.run()

