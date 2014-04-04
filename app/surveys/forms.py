from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, IntegerField
from wtforms.validators import Required
from wtforms.validators import Optional

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
