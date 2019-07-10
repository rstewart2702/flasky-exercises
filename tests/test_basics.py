import unittest
from flask import current_app
from app iport create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        # Tries to create an environment for the test that's close to what
        # we have in a running application.
	# 
        self.app = create_app('testing')          # create an application configured for testing
	self.app_context = self.app.app_context() # activate the application's context
	self.app_context.push()                   # 
	db.create_all()

    def tearDown(self):
        # Removes the database and application context "built out" by setUp(), above.
        db.session.remove()
	db.drop_all()
	self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
