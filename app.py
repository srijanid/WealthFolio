from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flaskuser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE'] = 'AI_Wealth_Manager'

mysql = MySQL(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Wealth Manager API!"}), 200

@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT VERSION()")  # Simple query to check the connection
        version = cursor.fetchone()
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

        cursor = mysql.connection.cursor()
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

if __name__ == '__main__':
    app.run(debug=True)
