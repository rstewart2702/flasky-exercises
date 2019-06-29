import os

from flask import Flask, render_template, abort, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Forms help and support:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

# This allows a "page-loaded" time to be propagated to the page,
# expressed in UTC, and the Moment.js Javascript can then be
# pushed to user pages to get the browser client to calculated
# how much time has elapsed since page load took place...
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# N.B. this is really just an example of how it might be done,
# and the real SECRET_KEY of a real application would likely be
# set up via an environment variable or some other mechanism
# that's easier to secure properly from prying eyes.
#
# An application SECRET_KEY is used by the form-handling to protect
# from cross-site request forgery, CSRF.
app.config['SECRET_KEY']='hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Each web-form is represented by an instance of a class derived
# from FlaskForm.
# The class defines the list of fields in the form, each
# represented by an object.  Each field object can have
# one or more validators attached.  A validator is a function
# that checks whether or not the data submitted by the user
# are valid.
#
# The fields in the form are defined as class variables.
# Each class variable is assigned an object associated with a field
# type.
#
# Form fields are callables that, when invoked from a template, render
# themselves to HTML.
#
# So, in the form-representing class below, instances of NameForm
# will have access to the fields called "name" and "submit"
# and the Jinja2 templating engine will use reflection capabilities
# (I guess?) to deduce the form constituent parts, and render the
# appropriate HTML.
# 
class NameForm(FlaskForm):
    name = \
    StringField(
        'What is your name',
        validators = [DataRequired()]
        )
    submit = \
    SubmitField('Submit')

# Database-related classes:
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #
    # for "referential integrity" and for ooey-gooey orm-ness:
    users = db.relationship('User', backref = 'role', lazy='dynamic')
    #
    def __repr__(self):
        return '<Role %r>' % self.name
    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    #
    # for 'referential integrity' and ooey-gooey orm-ness:
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 
    #
    def __repr__(self):
        return '<User %r>' % self.username
    


bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        #
        session['name'] = form.name.data
        form.name.data = ''
        # Again, this is here to implment post-redirect-get cycle.
        # Also, the data stored in "session-key" 'known' provides
        # the way for the subsequent GET-handling respond according
        # to whether or not the name is "brand new" or has been
        # stored in the past!
        return redirect(url_for('index'))
    #
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known',False),
        current_time = datetime.utcnow()
    )



@app.route('/user/<IName>')
def user(IName):
    return render_template('user.html', name=IName)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/test-err500')
def test_err500():
    abort(500)

@app.route('/test-err404')
def test_err404():
    abort(404)
