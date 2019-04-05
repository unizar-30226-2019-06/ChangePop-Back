from flask import render_template
from flask import Flask
from ChangePop import user
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.drop_all()
db.create_all()

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
#CsrfProtect(app)                       Esto aun no podemos k no tenemos ni key ni na


app.register_blueprint(user.bp)


@app.route('/')
def show():
    return render_template('index.html')


@app.route('/<path:subpath>')
def show2(subpath):
    return render_template(subpath+'.html')


def get_app():
    return app
