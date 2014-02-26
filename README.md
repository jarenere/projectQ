frame_game_theory
=================


Rrequirement
=================
flask 0.10.1
sqlalchemy 0.9.1
flask-sqlalchemy 1.0
flask-migrate  1.2.0
flask-wtf
bootstrap 2.3.2
Flask-Login-0.2.9.tar.gz
Flask-OpenID-1.2.1
flask-pagedown-0.1.3
Flask-Markdown-0.3
forgery forgerypy (to testing)
Flask-Bootstrap-3.1.1.1

Change Python default encoding:

create /Library/Python/2.7/site-packages/sitecustomize.py
Add below lines: 
import sys
sys.setdefaultencoding('utf-8')

Use
===
Run migration:

./manage.py db init
./manage.py db migrate
./manage.py db upgrade

Run server 
==========
./manage.py runserver