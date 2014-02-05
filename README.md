frame_game_theory
=================


Rrequirement
=================
flask 0.10.1
sqlalchemy 0.9.1
flask-sqlalchemy 1.0
flask-migrate  1.2.0
flask-wtf

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