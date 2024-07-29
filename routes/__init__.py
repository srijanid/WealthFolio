from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)
test_bp = Blueprint('test_bp',__name__)

from . import auth, user,test
