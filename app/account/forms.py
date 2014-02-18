from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, IntegerField
from wtforms.validators import Required
from wtforms.validators import Optional

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class AnswerNumericalForm(Form):
    answer = IntegerField('Answer')

class AnswerYNForm(Form):
    answer = RadioField('Answer', choices = [('Yes','Yes'),('No','No')])

class AnswerTextForm(Form):
    answer = TextField('Answer')

class AnswerChoiceForm(Form):
    answer = RadioField('Answer')

class AnswerForm(Form):
    pass

