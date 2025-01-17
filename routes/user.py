import datetime
from flask import request, jsonify, Blueprint
from middleware import verify_client_credentials
from models import OAuth2Token, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/test', methods=['GET'])
def test():
    return "Blueprint is working!"



