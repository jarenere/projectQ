Swarm_Surveys
=================


Requirement
=================
file requeriments.txt
pip install -r requeriments.txt



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

note:custom migration/envy.py for upgrade

Run server 
==========
./manage.py runserver