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

#flask-babel
from flask.ext.babel import Babel
babel = Babel(app)


# Dir to stats
stats_csv = os.path.join(basedir, 'stats_csv')
if not os.path.exists(stats_csv):
    os.makedirs(stats_csv)

# from app import models
# from app import views

from app.researcher import blueprint as researcher_blueprint
app.register_blueprint(researcher_blueprint, url_prefix='/researcher')

from app.surveys import blueprint as surveys_blueprint
app.register_blueprint(surveys_blueprint, url_prefix='/surveys')

# from app.auth.views import blueprint as auth
# app.register_blueprint(auth, url_prefix='/auth')

from app.auth import blueprint as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.stats import blueprint as stats_blueprint
app.register_blueprint(stats_blueprint, url_prefix='/stats')

from app.main import blueprint as main_blueprint
app.register_blueprint(main_blueprint)

from app.feedback import blueprint as feedback_blueprint
app.register_blueprint(feedback_blueprint, url_prefix='/feedback')


from datetime import datetime
from apscheduler.scheduler import Scheduler
from scheduler import deleteAnswers

# from app.stats.matching import Games
# app.game = Games(1)

# Start the scheduler
sched = Scheduler()
sched.start()
sched.add_interval_job(deleteAnswers.deleteAnswers, hours=2)

def status_part2(status):
    from app.models import StateSurvey
    if status & StateSurvey.PART2_MONEY:
        return u'Money Real'
    else:
        return u'Untrue money'


def status_part3(status):
    from app.models import StateSurvey
    if status & StateSurvey.PART3_MONEY:
        return u'Money Real'
    else:
        return u'Untrue money'


# app.jinja_env.globals.update(status_part_two=status_part_two)
app.jinja_env.globals['status_part2'] = status_part2
app.jinja_env.globals['status_part3'] = status_part3