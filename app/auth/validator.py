from wtforms import ValidationError
from ..models import User
from flask.ext.babel import gettext


class ValidateEmail(object):
    '''check if the answer is the expected
    '''
    def __init__(self, message=None):
        if not message:
            self.message = gettext('Email already registered.')
        else:  # pragma: no cover
            self.message = message
    
    def __call__(self, form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)

class ValidateDNI(object):
    '''check if the answer is the expected
    '''
    def __init__(self, message=None):
        if not message:
            self.message = gettext('Email already registered.')
        else:  # pragma: no cover
            self.message = message
    
    def __call__(self, form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)