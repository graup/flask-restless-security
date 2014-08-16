from flask import Flask, render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore, Security, \
		login_required, current_user, logout_user
from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException
from flask.ext.login import user_logged_in
from datetime import timedelta
from flask_jwt import JWT, jwt_required

# Create app  =================================================================
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'afhkhu2[]=426574hjksbsdhkj24787864329867324mm...//'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=60)

# Create database connection object  ==========================================
db = SQLAlchemy(app)

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

# Setup =======================================================================
@app.before_first_request
def create_user():
	db.create_all()

	# Create some initial users to test
	if db.session.query(User).count() == 0:
		user_datastore.create_user(email='test', password='test')
		user_datastore.create_user(email='test2', password='test2')
		stuff = SomeStuff(data1=2, data2='toto', user_id=1)
		db.session.add(stuff)
		stuff = SomeStuff(data1=5, data2='titi', user_id=1)
		db.session.add(stuff)
		db.session.commit()

if __name__ == '__main__':
	# Import models here to avoid circular imports
	from models import User, Role, SomeStuff

	# Setup Flask-Security  ===================================================
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	security = Security(app, user_datastore)

	# Setup API  ==============================================================
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

	app.run()