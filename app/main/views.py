from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .forms import NameForm
from ..email import send_email
from .. import db
from ..models import User

# N.B. now, the route-decorator comes from the blueprint, in this case, "main."
@main.route('/', methods=['GET','POST'])
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
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
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
        # 
        # Now that we're using a flask blueprint, the template resides
        # in a namespace; in this case, it'd be main.index, so that's
        # why we say '.index' here:
        return redirect(url_for('.index'))
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
            
