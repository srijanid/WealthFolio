import datetime
import uuid
from flask import request, jsonify, redirect, url_for
from middleware import verify_client_credentials
from . import auth_bp
from models import OAuth2Token, db, OAuth2Client, User
from flask_jwt_extended import create_access_token, jwt_required
import Password
from urllib.parse import urlencode
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

@auth_bp.route('/protected', methods=['GET'])
@verify_client_credentials
def protected_route():
    return jsonify({"message": "Client credentials verified successfully"}), 200

# Routes
@auth_bp.route('/auth', methods=['GET'])
def auth():
    client_id = str(uuid.uuid4())
    client_secret = str(uuid.uuid4())
    client_metadata = 'metadata about the client'

    new_client = OAuth2Client(client_id=client_id, client_secret=client_secret, client_metadata=client_metadata)
    db.session.add(new_client)
    db.session.commit()

    # Debugging line to confirm client creation
    created_client = OAuth2Client.query.filter_by(client_id=client_id).first()
    if created_client:
        print(f"Client successfully created: {created_client}")
    else:
        print("Client creation failed")

    query_params = urlencode({'client_id': client_id, 'client_secret': client_secret})
    redirect_url = f'/register?{query_params}'
    print(f"Redirecting to: {redirect_url}")  # Debugging line
    return redirect(redirect_url)


@auth_bp.route('/register', methods=['GET'])
@verify_client_credentials
def register():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    
    if not client_id or not client_secret:
        return jsonify({"message": "Client ID and Client Secret are required"}), 400

    print(f"Client ID: {client_id}, Client Secret: {client_secret}")  # Debugging line
    return f'Registration Page - Client ID: {client_id}, Client Secret: {client_secret}'


@auth_bp.route('/signup', methods=['POST'])
@verify_client_credentials
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ['FirstName', 'LastName', 'UserName', 'Email', 'PasswordHash', 'client_id', 'client_secret']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' is required"}), 400

    client_id = data['client_id']
    client_secret = data['client_secret']

    # Debugging lines to print received client_id and client_secret
    print(f"Received Client ID: {client_id}")
    print(f"Received Client Secret: {client_secret}")

    # Verify client ID and secret
    client = OAuth2Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()
    # Debugging line to print the result of the query
    if client:
        print(f"Client found: {client}")
    else:
        print("Client not found")
    if not client:
        return jsonify({"message": "Invalid client ID or secret"}), 401

    FirstName = data['FirstName']
    LastName = data['LastName']
    UserName = data['UserName']
    Email = data['Email']
    PasswordHash = data['PasswordHash']

    existing_user = User.query.filter_by(Email=Email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = Password.hash_password(PasswordHash)

    new_user = User(
        FirstName=FirstName,
        LastName=LastName,
        UserName=UserName,
        Email=Email,
        PasswordHash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    # Update the OAuth2Client entry with the user ID
    client.UserID = new_user.UserID
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/signin', methods=['POST'])
@verify_client_credentials
def signin():
    data = request.get_json()
    
    # Validate request data
    required_fields = [
        'client_id', 
        'client_secret', 
        'Email', 'PasswordHash']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' is required"}), 400

    client_id = data['client_id']
    client_secret = data['client_secret']
    Email = data['Email']
    PasswordHash = data['PasswordHash']

    # Debugging lines to verify the received credentials
    print(f"Received Client ID: {client_id}, Client Secret: {client_secret}")

    client = OAuth2Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()
     # Debugging line to verify if client is found
    if client:
        print(f"Client found: {client.client_id}")
    else:
        print("Client not found")

    if not client:
        return jsonify({"message": "Access denied: Invalid client credentials"}), 401

    existing_user = User.query.filter_by(Email=Email).first()

    if existing_user:
        print(f"User found: {existing_user.UserID}")
        if Password.verify_password(existing_user.PasswordHash, PasswordHash):
            print("Password is correct")
        else:
            print("Password is incorrect")
    else:
        print("User not found")

    if not existing_user or not Password.verify_password(existing_user.PasswordHash, PasswordHash):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=existing_user.UserID)

    new_token = OAuth2Token(
        client_id=client_id,
        UserID=existing_user.UserID,
        token_type='Bearer',
        access_token=access_token,
        issued_at=int(datetime.datetime.utcnow().timestamp()),
        expires_in=86400  # 24 hour expiration time
    )
    db.session.add(new_token)
    db.session.commit()

    return jsonify(access_token=access_token),200

@auth_bp.route('/profile', methods=['GET'])
@verify_client_credentials
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()

    # Retrieve user data from the database
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Return the user's profile data
    return jsonify({
        "username": user.UserName,  # Ensure correct field names
        "email": user.Email,
        # Add more fields as needed
    }), 200

@auth_bp.route('/profile/<int:user_id>', methods=['POST'])
@verify_client_credentials
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

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "user_id": user.UserID}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating profile", "error": str(e)}), 500

@auth_bp.route('/signout', methods=['POST'])
@verify_client_credentials
@jwt_required()
def signout():
    current_user_id = get_jwt_identity()
    jti = get_jwt()['jti']  # Get the unique identifier for the JWT
    token = OAuth2Token.query.filter_by(UserID=current_user_id, access_token=jti).first()

    if token:
        token.revoked = True
        token.access_token_revoked_at = int(datetime.datetime.utcnow().timestamp())
        db.session.commit()

    return jsonify({"message": "Signed out"}), 200
    