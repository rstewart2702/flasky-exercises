from flask import current_app, render_template
from . import mail

# Adding in support for sending email, particularly to site administration:
from flask_mail import Mail
from flask_mail import Message

# Need thread support in order to email asynchronously:
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = \
      Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
              sender = app.config['FLASKY_MAIL_SENDER'],
              recipients = [to])
    # Notice that there are two different kinds of templates being used here.
    # Also, notice that the "kwargs" is used to flexibly provide a dictionary
    # of (parameter,value) pairs to the render_template function:
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 
    # Now, use a background thread to send off the email:
    # Note that app is handed as a parameter to the send_async_email
    # function/procedure used within the thread, so that it's available
    # when the thread invokes function/procedure send_async_email.
    # THIS AIN'T NECESSARILY VERY SCALABLE:  IN GENERAL, A THREAD POOL
    # IS BETTER FOR THIS SORT OF THING, IF THERE WILL BE LOTS OF 
    # ASYNCHRONOUS EMAIL-SENDING!
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
