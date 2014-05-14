import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.script import Manager
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from flaskext.markdown import Markdown
from flask.ext.pagedown import PageDown
from flask.ext.bootstrap import Bootstrap
from flask.ext.babel import Babel


from config import config
config_name = 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)


bootstrap = Bootstrap()
bootstrap.init_app(app)

#markdown editor
pagedown = PageDown()
markdown = Markdown(app)
pagedown.init_app(app)

#OpenID
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
#flask-babel
babel = Babel(app)


db = SQLAlchemy(app)

# Dir to stats
stats_csv = os.path.join(basedir, 'stats_csv')
if not os.path.exists(stats_csv):
    os.makedirs(stats_csv)


# from datetime import datetime
# from apscheduler.scheduler import Scheduler
# from scheduler import deleteAnswers

# # Start the scheduler
# sched = Scheduler()
# sched.start()
# sched.add_interval_job(deleteAnswers.deleteAnswers, hours=2)

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