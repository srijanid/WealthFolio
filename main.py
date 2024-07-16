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
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
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
        cursor.execute("SELECT * FROM USERS")
        version = cursor.fetchall()
        cursor.close()
        return jsonify({"message": "Connected to MySQL!", "version": version[0]}), 200
    except Exception as e:
        return jsonify({"message": "Connection failed", "error": str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    username = data['username']
    email = data['email']
    password = data['password']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            cursor.close()
            return jsonify({"message": "User already exists"}), 409

        hashed_password = generate_password_hash(password, method='sha256')

        cursor.execute(
            "INSERT INTO users (firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
            (firstname, lastname, username, email, hashed_password)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return jsonify({"message": "User does not exist"}), 404

        if not check_password_hash(user[5], password):
            return jsonify({"message": "Invalid password"}), 401

        user_data = {
            "firstname": user[1],
            "lastname": user[2],
            "username": user[3],
            "email": user[4]
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
