from flask import Flask, render_template, abort
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


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
