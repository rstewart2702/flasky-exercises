from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required

from . import auth

from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')

    # N.B. flask expects templates' paths to be relative to the
    # application's templates directory.  So, we avoid naming collisions
    # with the main blueprint or other future blueprints that'll be added.
    return render_template('auth/login.html',form=form)

@auto.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
