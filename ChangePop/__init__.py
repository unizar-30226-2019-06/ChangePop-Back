from flask import render_template
from flask import Flask
from sqlalchemy.exc import OperationalError

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from ChangePop.exeptions import NotLoggedIn
login.unauthorized_handler(NotLoggedIn.not_auth_handler)

from ChangePop import models

#db.drop_all()

try:
    db.create_all()
    db.session.commit()
except OperationalError as e:
    print("Error BD: {}".format(e))

migrate = Migrate(app, db)

# CsrfProtect(app)                       Esto aun no podemos k no tenemos ni key ni na

from ChangePop import routes

def get_app():
    return app
