from flask import Blueprint
from .models import User

profile = Blueprint('profile', __name__, url_prefix='/profile')
