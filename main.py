from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = '100.122.226.52'
app.config['MYSQL_USER'] = 'anwesa'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anwesa:123@100.122.226.52/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
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
    Email = data['Email']
    PasswordHash = data['PasswordHash']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (Email,))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return jsonify({"message": "User does not exist"}), 404

        if not check_password_hash(user[5], PasswordHash):
            return jsonify({"message": "Invalid password"}), 401

        user_data = {
            "FirstName": user[1],
            "LastName": user[2],
            "UserName": user[3],
            "Email": user[4]
        }

        return jsonify({"message": "User signed in successfully", "user": user_data}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.DateOfBirth = request.form.get('dateofbirth')
        user.Address = request.form.get('address')
        user.City = request.form.get('city')
        user.State = request.form.get('state')
        user.ZipCode = request.form.get('zipcode')
        user.Country = request.form.get('country')
        user.PhoneNumber = request.form.get('phonenumber')

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
