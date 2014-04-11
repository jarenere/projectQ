from flask import Blueprint

blueprint = Blueprint('feedback', __name__)

from . import views
