import uuid
from flask import Flask, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlencode
from Queue_manager import request_queue_manager
from config import Config
from models import db
from routes import auth_bp, user_bp,test_bp
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
mysql = MySQL(app)

@app.route('/')
def home():
    return jsonify({"message": "Hello Users"}), 200

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(test_bp, url_prefix='/test')

@app.route('/some_route', methods=['POST'])
def some_route():
    # Example of how to add a request to the queue
    user_id = 1  # Replace with actual user ID
    req_data = {'key': 'value'}  # Replace with actual request data
    success, message = request_queue_manager.add_request(user_id, req_data)
    return jsonify({"message": message}), 200 if success else 400


if __name__ == '__main__':
    app.run(debug=True)