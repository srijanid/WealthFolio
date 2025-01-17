import datetime
from flask import request, jsonify, Blueprint
from middleware import verify_client_credentials
from models import OAuth2Token, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/test', methods=['GET'])
def test():
    return "Blueprint is working!"



<<<<<<< HEAD
@user_bp.route('/profile/<int:user_id>', methods=['POST'])
@jwt_required()
def update_profile(user_id):
    current_user_id = get_jwt_identity()

    # Ensure the current user is updating their own profile
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized access"}), 401

    # Get data from the request body
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Retrieve user data from the database
    user = User.query.get_or_404(user_id)

    # Update user profile fields based on the received data
    user.DateOfBirth = data.get('DateOfBirth', user.DateOfBirth)
    user.Address = data.get('Address', user.Address)
    user.City = data.get('City', user.City)
    user.State = data.get('State', user.State)
    user.ZipCode = data.get('ZipCode', user.ZipCode)
    user.Country = data.get('Country', user.Country)
    user.PhoneNumber = data.get('PhoneNumber', user.PhoneNumber)
    user.profile_image = data.get('profile_image', user.profile_image)

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "user_id": user.UserID}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating profile", "error": str(e)}), 500
=======
>>>>>>> fork/main
