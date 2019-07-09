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

# Adding in the Flask-migrate pieces:
from flask_migrate import Migrate

# Adding in support for the 
from flask_mail import Mail
from flask_mail import Message

#################################################################

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
    
################################################################################
#
# Configurations for mail support:
# N.B. store username and password in the enclosing environment,
# instead of in a configuration file or program file, eh?

app.config['MAIL_SERVER'] = 'mail.proassurance.com'
app.config['MAIL_PORT'] = 25 # deduced from an existing application's configuration file...
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')

# N.B. some environments don't require an email password, eh?
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flaskyadmin@example.com>'

app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

def send_email(to, subject, template, **kwargs):
    msg = \
      Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
              sender = app.config['FLASKY_MAIL_SENDER'],
              recipients = [to])
    # Notice that there are two different kinds of templates being used here.
    # Also, notice that the "kwargs" is used to flexibly provide a dictionary
    # of (parameter,value) pairs to the render_template function:
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


# "To expose the database migration commands, Flask-Migrate
# adds a flask db command with several subcommands...
migrate = Migrate(app, db)


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
            # The flash() function is invoked with a message to be displayed on
            # the next response sent back to the client!
            # Of course, a template must also be changed along with this,
            # in order to retrieve the accumulated message texts into a
            # rendered page.
            flash('Looks like you have changed your name!')
            flash('Feel free to change as often as necessary...')
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        #
        # If the user submitted data which passed validation,
        # then we wish to store the name field's data inside
        # a session-local variable called 'name' so that it
        # persists across invocations to this function, and
        # redirect the user's browser to the this same place
        # again, which will allow the form to be redisplayed
        # due to a GET request submitted by the browser,
        # because of the redirect.
        # This implements the "post-redirect-get" cycle.
        session['name'] = form.name.data
        return redirect(url_for('index'))
    #
    # N.B. session.get('name') will evaluate to None if there are no data
    # stored under the 'name' key within the session.
    # If we had written session['name'] instead, that expression could
    # result in an exception if there is no 'name' key within session.
    # Using the get() method is preferable.
    return render_template(
        'index.html',
        form = form,
        name = session.get('name'),
        known = session.get('known',False),
        current_time = datetime.utcnow()
    )

# This provides a "shell context processor," which is used by 
# Flask and/or flask-sqlalchemy in order to auto-matically/-magically
# provide references to the database instance and the model
# meta-objects, so that they're available for use when using the
# "flask shell" interactive prompt, etc:
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


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
