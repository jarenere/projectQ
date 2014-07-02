from flask import Blueprint

blueprint = Blueprint('stats', __name__)

from . import views
