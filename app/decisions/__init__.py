from flask import Blueprint

blueprint = Blueprint('decisions', __name__)

from . import views
