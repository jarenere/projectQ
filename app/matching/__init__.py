from flask import Blueprint

blueprint = Blueprint('matching', __name__)

from . import views
