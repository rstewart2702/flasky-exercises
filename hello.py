from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# This allows a "page-loaded" time to be propagated to the page,
# expressed in UTC, and the Moment.js Javascript can then be
# pushed to user pages to get the browser client to calculated
# how much time has elapsed since page load took place...
from datetime import datetime


app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html', current_time = datetime.utcnow())


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
