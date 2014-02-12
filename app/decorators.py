from flask.ext.login import current_user
from functools import wraps
from flask import render_template
from models import ROLE_ADMIN, ROLE_RESEARCHER, ROLE_USER


def researcher_required(f):  # pragma: no cover
    """Checks if the user is and researcher or not"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == ROLE_RESEARCHER:
            return f(*args, **kwargs)
        else:
            return render_template('403.html'), 403
    return decorated_function