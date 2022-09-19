from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET','POST')
def index():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        db.session.add(user)
        db.session.commit()
        session['known'] = False
        return redirect(url_for('.index')) #shorten version of 'main.index'
    return render_template('index.html',
                           current_time=datetime.utcnow(), 
                           form=form, name=session.get('name'), 
                           known=session.get('known', false))


