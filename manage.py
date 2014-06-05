#!/usr/bin/env python

# from app import app, manager
from app import app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand, Migrate
import os


# app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(use_ipython=True))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    COV = True
    if COV:
        import coverage
        cov = coverage.coverage(branch=True, include='app/*')
        cov.start()

    import unittest
    # tests = unittest.TestLoader().discover('testing_tests')
    tests = unittest.TestLoader().discover('tests')

    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()

@manager.command
def p80():
    app.run(port = 80, host='0.0.0.0')

@manager.command
def jmeter():
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['JMETER'] = True
    app.run(port = 80, host='0.0.0.0')

if __name__ == "__main__":
    manager.run()