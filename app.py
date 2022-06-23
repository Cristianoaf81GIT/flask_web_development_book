# -*- encoding: utf8 -*-
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your browser is {}!</h1>'.format(user_agent)


@app.route('/user/<name>')
def show_user_name(name):
    return '<h1>Hello, {}!</h1>'.format(name)


@app.route('/bad-request')
def bad_request_example():
    return '<h1>Bad request</h1', 400


@app.route('/cookies')
def cookies_demo():
    response = make_response(
        '<h1>this docs carries a cookie</h1>')
    response.set_cookie('answer', '42')
    response.content_type = "application/json"
    response.set_data('teste')
    return response


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
