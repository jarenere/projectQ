import unittest
from flask import current_app
from app import app,db
from app.models import User,ROLE_RESEARCHER
import os
from config import basedir

class UserTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        # create a user
        u = User(nickname = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()