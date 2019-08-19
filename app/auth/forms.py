from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from wtforms import ValidationError
from ..models import User

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

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), length(1,64), Email()])
    
    username = \
        StringField('Username',
                    validators = [DataRequired(), length(1,64),
                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                         'Usernames must have only letters, numbers, dots or '
                                         'underscores')])
    password = \
        PasswordField('Password',
                      validators = [DataRequired(),
                                    EqualTo('password2', message='Passwords must match.')])
    password2 = \
        PasswordField('Confirm Password',
                      validators = [DataRequired()])
    submit = SubmitField('Register')

    # Any method which has name which starts with "validate_" is invoked
    # via reflection features of Python in order to perform additional
    # per-field validation.
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')
