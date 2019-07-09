from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Each web-form is represented by an instance of a class derived
# from FlaskForm.
# The class defines the list of fields in the form, each
# represented by an object.  Each field object can have
# one or more validators attached.  A validator is a function
# that checks whether or not the data submitted by the user
# are valid.
#
# The fields in the form are defined as class variables.
# Each class variable is assigned an object associated with a field
# type.
#
# Form fields are callables that, when invoked from a template, render
# themselves to HTML.
#
# So, in the form-representing class below, instances of NameForm
# will have access to the fields called "name" and "submit"
# and the Jinja2 templating engine will use reflection capabilities
# (I guess?) to deduce the form constituent parts, and render the
# appropriate HTML.
#
class NameForm(FlaskForm):
    name = \
    StringField(
        'What is your name',
        validators = [DataRequired()]
        )
    submit = \
    SubmitField('Submit')

