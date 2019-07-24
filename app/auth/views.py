from flask import render_template

from . import auth

@auth.route('/login')
def login():
    # N.B. flask expects templates' paths to be relative to the
    # application's templates directory.  So, we avoid naming collisions
    # with the main blueprint or other future blueprints that'll be added.
    return render_template('auth/login.html')
