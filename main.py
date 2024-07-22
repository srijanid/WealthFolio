import datetime
import hashlib
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import time

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

# SQLAlchemy User Model
class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    UserName = db.Column(db.String(80), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(200), nullable=False)
    DateOfBirth = db.Column(db.String(80))
    Address = db.Column(db.String(200))
    City = db.Column(db.String(100))
    State = db.Column(db.String(100))
    ZipCode = db.Column(db.String(20))
    Country = db.Column(db.String(100))
    PhoneNumber = db.Column(db.String(20))
    Token = db.Column(db.String(500))

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Wealth Manager API!"}), 200

@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        version = cursor.fetchall()
        cursor.close()
        return jsonify({"message": "Connected to MySQL!", "version": version[0]}), 200
    except Exception as e:
        return jsonify({"message": "Connection failed", "error": str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        required_fields = ['FirstName', 'LastName', 'UserName', 'Email', 'PasswordHash']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"'{field}' is required"}), 400

        FirstName = data['FirstName']
        LastName = data['LastName']
        UserName = data['UserName']
        Email = data['Email']
        PasswordHash = data['PasswordHash']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = %s", (Email,))
        user = cursor.fetchone()
        if user:
            cursor.close()
            return jsonify({"message": "User already exists"}), 409

        hashed_password = generate_password_hash(PasswordHash, method='pbkdf2:sha256', salt_length=8)

        cursor.execute(
            "INSERT INTO users (FirstName, LastName, UserName, Email, PasswordHash) VALUES (%s, %s, %s, %s, %s)",
            (FirstName, LastName, UserName, Email, hashed_password)
        )
        time.sleep(5)
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "User registered successfully"}), 201
    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    Email = data.get('Email')  # Using get() to safely retrieve JSON data
    PasswordHash = data.get('PasswordHash')

    if not all([Email, PasswordHash]):
        return jsonify({"message": "Email and password are required"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = %s", (Email,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({"message": "User does not exist"}), 404

        stored_password_hash = user[5]  # Assuming PasswordHash is at index 5

        if not stored_password_hash or not isinstance(stored_password_hash, str):
            return jsonify({"message": "Invalid stored password hash"}), 500

        if not check_password_hash(stored_password_hash, PasswordHash):
            return jsonify({"message": "Invalid password"}), 401

        # Create access token
        access_token = create_access_token(identity=user[0],expires_delta=datetime.timedelta(minutes=10))  # Assuming UserID is at index 0

        # Save the token to the database
        user_obj = User.query.get(user[0])
        user_obj.Token = access_token
        db.session.commit()

        user_data = {
            "FirstName": user[1],    # Assuming Firstname is at index 1
            "LastName": user[2],     # Assuming LastName is at index 2
            "UserName": user[3],     # Assuming UserName is at index 3
            "Email": user[4]         # Assuming Email is at index 4
        }

        return jsonify({"message": "User signed in successfully", "user": user_data, "access_token": access_token}), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

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
