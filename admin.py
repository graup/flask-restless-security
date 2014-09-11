from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import BaseView, expose
from flask.ext.security import current_user
from flask import redirect
from flask.ext.security import logout_user

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_visible(self):
    	return current_user.is_authenticated()

class LoginView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login?next=/admin')

    def is_visible(self):
    	return not current_user.is_authenticated()

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

class UserModelView(AdminModelView):
	column_list = ('email', 'active', 'last_login_at', 'roles', )
