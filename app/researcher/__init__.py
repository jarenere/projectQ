from flask import Blueprint

blueprint = Blueprint('researcher', __name__)

from . import views
