from flask import Flask, render_template
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html', title='Strona główna', currentTime=datetime.utcnow())

# @app.route('user/name')
# def user(name):
#     return '<h1>Witaj, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run()

