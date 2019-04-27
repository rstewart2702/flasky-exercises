from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Forms help and support:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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


# This allows a "page-loaded" time to be propagated to the page,
# expressed in UTC, and the Moment.js Javascript can then be
# pushed to user pages to get the browser client to calculated
# how much time has elapsed since page load took place...
from datetime import datetime


app = Flask(__name__)
# N.B. this is really just an example of how it might be done,
# and the real SECRET_KEY of a real application would likely be
# set up via an environment variable or some other mechanism
# that's easier to secure properly from prying eyes.
#
# An application SECRET_KEY is used by the form-handling to protect
# from cross-site request forgery, CSRF.
app.config['SECRET_KEY']='hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template(
        'index.html',
        form = form,
        name = name,
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
