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


fixed
=====

Si falla al iniciar sesión, forzar str en la comparacion en el fichero: werkzeug/security.py


        return _builtin_safe_str_cmp(a, str(b))

        
https://github.com/mitsuhiko/werkzeug/issues/537

Run server 
==========
./manage.py runserver