from flask import Blueprint, request, jsonify
from models import Reminder
from models import db

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/reminders', methods=['GET'])
def get_reminders():
    # Retrieve all reminders
    pass

@reminders_bp.route('/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    # Retrieve specific reminder
    pass

@reminders_bp.route('/reminders', methods=['POST'])
def create_reminder():
    # Create new reminder
    pass

@reminders_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    # Update reminder
    pass

@reminders_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    # Delete reminder
    pass
