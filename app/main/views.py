from datetime import datetime
from flask import render_template
from . import main

# Now that we are on the way towards adding in fully-developed user-handling,
# and implementing the user-login capabilities that are typical in most
# websites, the view functions herein need to change substantially.
#
# This means that all of the former checking for the user's presence in the current
# session is not going to make sense going forward, so it needs to be removed/simplified.

@main.route('/')
def index():
    return render_template('index.html', current_time = datetime.utcnow())

