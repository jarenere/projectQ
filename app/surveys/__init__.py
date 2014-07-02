from flask import Blueprint

blueprint = Blueprint('surveys', __name__)

from . import views
