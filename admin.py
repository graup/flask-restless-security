from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from flask_security import current_user
from flask import redirect
from flask_security import logout_user

from application import app
from database import db
from models import User, Role, SomeStuff


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_visible(self):
        return current_user.is_authenticated


class LoginView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login?next=/admin')

    def is_visible(self):
        return not current_user.is_authenticated


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class UserModelView(AdminModelView):
    column_list = ('email', 'active', 'last_login_at', 'roles', )


def init_admin():
    admin = Admin(app)
    admin.add_view(UserModelView(User, db.session, category='Auth'))
    admin.add_view(AdminModelView(Role, db.session, category='Auth'))
    admin.add_view(AdminModelView(SomeStuff, db.session))
    admin.add_view(LogoutView(name='Logout', endpoint='logout'))
    admin.add_view(LoginView(name='Login', endpoint='login'))
