import sqlite3

import sqlalchemy
from flask import render_template
from flask import Flask
from sqlalchemy.exc import OperationalError

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
migrate = Migrate(app, db)

from ChangePop import models

manager = Manager(app)
manager.add_command('db', MigrateCommand)

try:
    fh = open('./app.db', 'r')

except FileNotFoundError:
    db.create_all()

manager.add_command('db', MigrateCommand)

from flask import g
from flask.sessions import SecureCookieSessionInterface


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                             **kwargs)


app.session_interface = CustomSessionInterface()


from ChangePop.exeptions import NotLoggedIn
login.unauthorized_handler(NotLoggedIn.not_auth_handler)


# CsrfProtect(app)                       Esto aun no podemos k no tenemos ni key ni na

from ChangePop import routes

def get_app():
    return app
