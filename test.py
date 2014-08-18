import os
from server import app, init_app, user_datastore
from database import db
import unittest
import tempfile
import re

from flask.ext.security import current_user
from flask.ext.security.utils import login_user
from models import User, Role, SomeStuff

class FlaskTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, self.db_path = tempfile.mkstemp()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
		app.config['TESTING'] = True
		app.config['DEBUG'] = True
		self.client = app.test_client()
		self._ctx = app.test_request_context()
		self._ctx.push()

		with app.app_context():
			init_app()
			user_datastore.create_user(email='test', password='test')
			db.session.commit()

	def tearDown(self):
		if self._ctx is not None:
			self._ctx.pop()
		with app.app_context():
			db.session.remove()
			db.drop_all()
			os.close(self.db_fd)
        	os.unlink(self.db_path)

	def _post(self, route, data=None, content_type=None, follow_redirects=True, headers=None):
		content_type = content_type or 'application/x-www-form-urlencoded'
		return self.client.post(route, data=data, follow_redirects=follow_redirects, content_type=content_type, headers=headers)

	def _login(self, email=None, password=None):
		csrf_token = ''
		rv = self.client.get('/login')
		matches = re.findall('name="csrf_token".*?value="(.*?)"', rv.data)
		if matches:
			csrf_token = matches[0]

		email = email or 'test'
		password = password or 'test'
		data = {
			'email': email,
			'password': password,
			'remember': 'y',
			'csrf_token': csrf_token
			}
		return self._post('/login', data=data, follow_redirects=False)

class ViewsTest(FlaskTestCase):
	def test_protected_page(self):
		rv = self.client.get('/')
		assert 'Redirecting...' in rv.data

		self._login()

		rv = self.client.get('/')
		assert 'It works' in rv.data

if __name__ == '__main__':
	unittest.main()