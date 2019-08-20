from flask_mail import Message
from hello import mail

msg = Message(
        'test email',
        sender='richardstewart@proassurance.com',
        recipients=['richardstewart@proassurance.com'])

msg.body = 'This is the plain text body.'

msg.html = 'This is the <b>HTML</b> body.'

with app.app_context():
    mail.send(msg)
