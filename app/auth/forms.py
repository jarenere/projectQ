# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import TextField,StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from validator import ValidateEmail, ValidateDNI
from ..models import User


class LoginFormOpenID(Form):
    openid = TextField(gettext('openid'), validators = [Required()])
    remember_me = BooleanField(gettext('Keep me logged in'), default = False)

class LoginFormEmail(Form):
    email = StringField(gettext('Email'), validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(gettext('Contraseña'), validators=[Required()])
    remember_me = BooleanField(gettext('Identificarse automáticamente en cada visita'), default = False)
    submit = SubmitField(gettext('Iniciar sesión'))


class RegistrationForm(Form):
    email = StringField(gettext('Email'), validators=[Required(), Length(1, 64),
                                           Email(), ValidateEmail()])
    submit = SubmitField(gettext('Register'))


class DatesForm(Form):
    name = TextField(gettext('Name'), validators = [Required()])
    last_name = TextField(gettext('Last name'), validators = [Required()])
    dni = TextField(gettext('dni'), validators = [Required(),ValidateDNI()])



class RegistrationForm2(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField('Contraseña', validators=[
        Required(), EqualTo('password2', message='Las contraseñas deben coincidir.')])
    password2 = PasswordField('Confirmar contaseña', validators=[Required()])
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Correo ya registrado.')