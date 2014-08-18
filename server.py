from flask import Flask, render_template, request, url_for, redirect
from flask.ext.security import SQLAlchemyUserDatastore, Security, \
		login_required, current_user, logout_user
from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException
from flask.ext.login import user_logged_in
from datetime import timedelta
from flask_jwt import JWT, jwt_required

from database import db
from models import User, Role, SomeStuff, user_datastore

# Create app  =================================================================
app = Flask(__name__)
app.config['APP_NAME'] = 'ApplicationName'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'afhkhu2[]=426574hjksbsdhkj24787864329867324mm...//'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=60)
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_TRACKABLE'] = True

# Setup Flask-Security  =======================================================
security = Security(app, user_datastore)

# JWT Token authentication  ===================================================
jwt = JWT(app)
@jwt.authentication_handler
def authenticate(username, password):
	user = user_datastore.find_user(email=username)
	print '%s vs. %s' % (username, user.email)
	if username == user.email and password == user.password:
		return user
	return None

@jwt.user_handler
def load_user(payload):
	user = user_datastore.find_user(id=payload['user_id'])
	return user

# Flask-Restless API  =========================================================
@jwt_required()
def auth_func(**kw):
	return True

# Views  ======================================================================
@app.route('/')
@login_required
def home():
	print(request.headers)
	return render_template('index.html')

@app.route('/logout/')
def log_out():
	logout_user()
	return redirect(request.args.get('next') or '/')

# Setup API  ==================================================================
apimanager = APIManager(app, flask_sqlalchemy_db=db)
apimanager.create_api(SomeStuff,
	methods=['GET', 'POST', 'DELETE', 'PUT'],
	url_prefix='/api/v1',
	collection_name='free_stuff',
	include_columns=['data1', 'data2', 'user_id'])
apimanager.create_api(SomeStuff,
	methods=['GET', 'POST', 'DELETE', 'PUT'],
	url_prefix='/api/v1',
	preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]),
	collection_name='protected_stuff',
	include_columns=['data1', 'data2', 'user_id'])

# Bootstrap  ==================================================================
def init_app():
	db.init_app(app)
	db.create_all()

def create_test_models():
	user_datastore.create_user(email='test', password='test')
	user_datastore.create_user(email='test2', password='test2')
	stuff = SomeStuff(data1=2, data2='toto', user_id=1)
	db.session.add(stuff)
	stuff = SomeStuff(data1=5, data2='titi', user_id=1)
	db.session.add(stuff)
	db.session.commit()

@app.before_first_request
def bootstrap_app():
	if not app.config['TESTING']:
		if db.session.query(User).count() == 0:
			create_test_models();

with app.app_context():
	init_app()

# Start server  ===============================================================
if __name__ == '__main__':		
	app.run()
