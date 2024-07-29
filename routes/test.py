from flask import Blueprint, jsonify
from models import db
from . import test_bp


@test_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Wealth Manager API!"}), 200

@test_bp.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM users")
        version = cursor.fetchall()
        cursor.close()
        return jsonify({"message": "Connected to MySQL!", "version": version[0]}), 200
    except Exception as e:
        return jsonify({"message": "Connection failed", "error": str(e)}), 500