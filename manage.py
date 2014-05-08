#!flask/bin/python

# from app import app, manager
from app import app
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand
import os

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    COV = True
    if COV:
        import coverage
        COV = coverage.coverage(branch=True, include='app/*')
        COV.start()

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
if __name__ == "__main__":
    app.debug = True
    manager.run()