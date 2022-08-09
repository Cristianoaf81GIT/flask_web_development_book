# -*- encoding: utf8 -*-
from flask import Flask, request, make_response, redirect,abort, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy


class NameForm(FlaskForm):
    name = StringField('what is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

baseDir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']=\
        'sqlite:///' + os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# entity user role
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name

# entity user
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template(
            'index.html', 
            current_time=datetime.utcnow(), form=form, name=session.get('name'))


@app.route('/user/<name>')
def show_user_name(name):
    return render_template('user.html', name=name)


@app.route('/comments')
def show_comments():
    comments = ['ok', 'lets', 'go', 'python']
    return render_template('comments.html', comments=comments)


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


@app.route('/redirect-user')
def redirect_demo():
    return redirect('https://www.google.com.br')


@app.route('/users/<id>')
def abort_demo(id):
    if int(id) != 1:
        abort(404)
    return '<h1>Hello, cristiano</h1>'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
