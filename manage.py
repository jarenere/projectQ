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
        cov = coverage.coverage(branch=True, include='app/*')
        cov.start()

    import unittest
    # tests = unittest.TestLoader().discover('tests')
    tests = unittest.loader.discover('tests', pattern = "Test*.py") 
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
if __name__ == "__main__":
    app.debug = True
    manager.run()