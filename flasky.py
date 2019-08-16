import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

# print("Current database url:  ", db.engine.url)

@app.shell_context_processor
def make_shell_context():
    # These two execute successfully when you start up the flask "environment"
    # at a command prompt, but they can't be used outside this context,
    # for example, in the preceding lines, because the necessary object instances
    # don't yet exist.  So, such output lines should be used elsewhere,
    # perhaps inside of some part of the app initialization or something?
    print("Running with configuration:  ",(os.getenv('FLASK_CONFIG') or 'default'))
    print("Current database url:  ", db.engine.url)

    return dict(db=db, User=User, Role=Role)

# The app.cli.command decorator allows us to implement
# custom commands within Flask.
# So, this adds a command named 'test' that can be 
# executed from the command-line like so:
#   flask test
#
@app.cli.command()
def test(): 
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
