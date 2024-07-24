from flask import Flask, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from flask_oauthlib.provider import OAuth2Provider
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = '100.122.226.52'
app.config['MYSQL_USER'] = 'anwesa'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'wealthapp'
mysql = MySQL(app)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anwesa:123@100.122.226.52/wealthapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# JWT configurations
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key in production
jwt = JWTManager(app)

oauth = OAuth2Provider(app)

# Define the database models
class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.String(255))
    City = db.Column(db.String(50))
    State = db.Column(db.String(50))
    ZipCode = db.Column(db.String(10))
    Country = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(20))
    DateOfRegistration = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class OAuth2Client(db.Model):
    client_id = db.Column(db.String(48), primary_key=True)
    client_secret = db.Column(db.String(120), nullable=False)
    client_metadata = db.Column(db.Text, nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))

class OAuth2Token(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String(48), db.ForeignKey('oauth2client.client_id'))
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    scope = db.Column(db.Text)
    revoked = db.Column(db.Boolean, default=False)
    issued_at = db.Column(db.Integer)
    expires_in = db.Column(db.Integer)
    access_token_revoked_at = db.Column(db.Integer)
    refresh_token_revoked_at = db.Column(db.Integer)

# Middleware to verify client credentials
@app.before_request
def verify_client_credentials():
    if request.endpoint not in ['auth', 'signup', 'signin']:
        client_id = request.headers.get('Client-ID')
        client_secret = request.headers.get('Client-Secret')
        if not client_id or not client_secret:
            return jsonify({"message": "Client credentials required"}), 401
        client = OAuth2Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()
        if not client:
            return jsonify({"message": "Invalid client credentials"}), 401

# Routes
@app.route('/auth')
def auth():
    # Here you would generate client_id and client_secret and store them
    client_id = 'generated_client_id'
    client_secret = 'generated_client_secret'
    client_metadata = 'metadata about the client'
    
    new_client = OAuth2Client(client_id=client_id, client_secret=client_secret, client_metadata=client_metadata)
    db.session.add(new_client)
    db.session.commit()
    
    return redirect(url_for('register', client_id=client_id, client_secret=client_secret))

@app.route('/register' ,methods=['GET'])
def register():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    # Render registration page with client info (this is just an example)
    return f'Registration Page - Client ID: {client_id}, Client Secret: {client_secret}'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ['FirstName', 'LastName', 'Email', 'Password']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"'{field}' is required"}), 400

    FirstName = data['FirstName']
    LastName = data['LastName']
    Email = data['Email']
    Password = data['Password']

    existing_user = User.query.filter_by(Email=Email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = generate_password_hash(Password, method='pbkdf2:sha256', salt_length=8)

    new_user = User(
        FirstName=FirstName,
        LastName=LastName,
        Email=Email,
        PasswordHash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/signin', methods=['POST'])
def signin():
    client_id = request.json.get('client_id')
    client_secret = request.json.get('client_secret')
    username = request.json.get('username')
    password = request.json.get('password')

    client = OAuth2Client.query.filter_by(client_id=client_id, client_secret=client_secret).first()
    if not client:
        return jsonify({"message": "Access denied: Invalid client credentials"}), 401

    user = User.query.filter_by(Email=username).first()
    if not user or not check_password_hash(user.PasswordHash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.UserID)
    
    new_token = OAuth2Token(
        client_id=client_id,
        UserID=user.UserID,
        token_type='Bearer',
        access_token=access_token,
        issued_at=int(datetime.datetime.utcnow().timestamp()),
        expires_in=3600  # 1 hour expiration time
    )
    db.session.add(new_token)
    db.session.commit()

    return jsonify(access_token=access_token)

@app.route('/signout', methods=['POST'])
@jwt_required()
def signout():
    current_user = get_jwt_identity()
    token = OAuth2Token.query.filter_by(UserID=current_user, access_token=get_jwt()['jti']).first()
    if token:
        token.revoked = True
        token.access_token_revoked_at = int(datetime.datetime.utcnow().timestamp())
        db.session.commit()
    return jsonify({"message": "Signed out"}), 200

@app.route('/profile/<int:user_id>', methods=['POST'])
@jwt_required()
def update_profile(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized access"}), 401

    user = User.query.get_or_404(user_id)

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

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

if __name__ == '__main__':
    app.run(debug=True)
