import os
from server import app, init_app
import unittest
import tempfile
from models import User, Role, SomeStuff

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class ViewsTest(FlaskTestCase):
	def test_something(self):
		rv = self.app.get('/')
		assert 'Redirecting...' in rv.data

if __name__ == '__main__':
    unittest.main()