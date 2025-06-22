from flask import session, redirect, url_for, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from functools import wraps

from bot.db.session import async_session

# -- маленький декоратор для захисту
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated

class SecureIndexView(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        return super().index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get("logged_in")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))

    # DB-сесія для моделі
    def get_session(self):
        return async_session
