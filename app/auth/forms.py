from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    # This email field uses the Length() and Email() validators
    # in addition to DataRequired(), to ensure that the user
    # not only provides an email address value that is valid.
    # WTForms evaluates the validators in the order they are
    # provided here, and will stop at the first validation
    # failure it encounters.
    email = \
        StringField('Email',
                    validators=[DataRequired(),
                                Length(1,64),
                                Email()] )
    #
    # This represents an <input> element with type="password".
    password = \
        PasswordField('Password',
                      validators=[DataRequired()])
    #
    # The following represents a checkbox:
    remember_me = BooleanField('Keep me logged in')
    #
    submit = SubmitField('Log In')
