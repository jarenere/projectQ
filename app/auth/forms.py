from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms.validators import Required, Email, Length
from wtforms import TextField,StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email
from validator import ValidateEmail, ValidateDNI


class LoginFormOpenID(Form):
    openid = TextField(gettext('openid'), validators = [Required()])
    remember_me = BooleanField(gettext('Keep me logged in'), default = False)

class LoginFormEmail(Form):
    email = StringField(gettext('Email'), validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(gettext('Password'), validators=[Required()])
    remember_me = BooleanField(gettext('Keep me logged in'), default = False)
    submit = SubmitField(gettext('Log In'))


class RegistrationForm(Form):
    email = StringField(gettext('Email'), validators=[Required(), Length(1, 64),
                                           Email(), ValidateEmail()])
    submit = SubmitField(gettext('Register'))


class DatesForm(Form):
    name = TextField(gettext('Name'), validators = [Required()])
    last_name = TextField(gettext('Last name'), validators = [Required()])
    dni = TextField(gettext('dni'), validators = [Required(),ValidateDNI()])


