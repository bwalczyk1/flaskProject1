from flask import Flask, render_template, request
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'dfghj765$%^Kjhgd'


class WeatherForm(FlaskForm):
    station = StringField('Podaj nazwę stacji: ', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


@app.route('/', methods=["POST", "GET"])
def index():
    weatherForm = WeatherForm()
    if request.method == "GET":
        return render_template('weather.html', title='Zadanie 2.1', weatherForm=weatherForm)

    f = open('weather.json')
    data = json.load(f)
    stationName = request.form['station']
    returnData = {"message": "Nie ma takiej stacji"}
    for station in data:
        if station["stacja"] == stationName:
            returnData = station
            break
    f.close()
    return render_template('weather.html', title='Zadanie 2.1', weatherForm=weatherForm, weatherData=returnData)

if __name__ == '__main__':
    app.run()

