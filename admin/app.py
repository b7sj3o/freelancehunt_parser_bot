import os
import sys
import argparse

from flask import Flask, render_template, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

from admin.config import ADMIN_HOST, ADMIN_PORT
from admin.views import SecureIndexView
from bot.db.models import User, Category, CategoryItem


app = Flask(__name__, static_folder="static/css", template_folder="templates")
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
admin = Admin(
    app,
    name="Telegram Bot Admin",
    base_template="admin/base.html",
    template_mode="bootstrap2",
)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(CategoryItem, db.session))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Run the server in debug mode",
    )
    args = parser.parse_args()

    app.run(host=ADMIN_HOST, port=ADMIN_PORT, debug=args.reload)
