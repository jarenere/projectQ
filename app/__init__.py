import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from flaskext.markdown import Markdown
from flask.ext.pagedown import PageDown
from flask.ext.bootstrap import Bootstrap



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

Bootstrap(app)
#markdown editor
pagedown = PageDown(app)
markdown = Markdown(app)

app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

#OpenID
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import models
from app import views

from app.researcher.researcher import blueprint as researcher
app.register_blueprint(researcher, url_prefix='/researcher')

from app.account.views import blueprint as account
app.register_blueprint(account, url_prefix='/account')

# from app.auth.views import blueprint as auth
# app.register_blueprint(auth, url_prefix='/auth')

from app.auth import blueprint as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')