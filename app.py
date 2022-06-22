# -*- encoding: utf8 -*-
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your browser is {}!</h1>'.format(user_agent)


@app.route('/user/<name>')
def show_user_name(name):
    return '<h1>Hello, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
