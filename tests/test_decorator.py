import unittest
from flask import current_app
from app import app,db
from app.models import User,ROLE_RESEARCHER
import os
from config import basedir

class DecoratorTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




if __name__ == '__main__':
    unittest.main()