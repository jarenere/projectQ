# -*- coding: utf-8 -*-
# ...
# available languages

import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Chamber of Secrets :D'
# config tu jmeter
JMETER = False
SEQUENCE = [5, 6, 7, 8, 9, 10, 17, 16, 12, 23, 22, 32, 33, 40, 41, 42, 49, 50, 51, 46, 47, 48, 14, 15]

basedir = os.path.abspath(os.path.dirname(__file__))

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}
LOCALES = ['en', 'es']