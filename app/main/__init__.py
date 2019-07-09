from flask import Blueprint

# Blueprints are created by instantiating an instance of Blueprint.
# The constructor takes two arguments, the blueprint name, and 
# the module or package where the blueprint is located.

main = Blueprint('main', __name__)
from . import views, errors
