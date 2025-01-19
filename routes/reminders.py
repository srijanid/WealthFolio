from flask import Blueprint, request, jsonify
from models import Reminder
from models import db
from . import auth_bp

#reminders_bp = Blueprint('reminders', __name__)

@auth_bp.route('/reminders', methods=['GET'])
# Retrieve all reminders for a user
def get_reminders_for_user(user_id):
    reminders = Reminder.query.filter_by(UserId=user_id).all()
    reminder_list = [{
        'ReminderId': reminder.ReminderId,
        'UserId': reminder.UserId,
        'BillId': reminder.BillId,
        'reminder_date': reminder.reminder_date,
        'message': reminder.message,
        'CreatedAt': reminder.CreatedAt,
        'UpdatedAt': reminder.UpdatedAt
    } for reminder in reminders]
    return jsonify(reminder_list), 200

@auth_bp.route('/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    # Retrieve specific reminder
    reminder = Reminder.query.get_or_404(reminder_id)
    reminder_data = {
        'ReminderId': reminder.ReminderId,
        'UserId': reminder.UserId,
        'BillId': reminder.BillId,
        'reminder_date': reminder.reminder_date,
        'message': reminder.message,
        'CreatedAt': reminder.CreatedAt,
        'UpdatedAt': reminder.UpdatedAt
    }
    return jsonify(reminder_data), 200

@auth_bp.route('/reminders', methods=['POST'])
def create_reminder():
    # Create new reminder
    data = request.json
    new_reminder = Reminder(
        UserId=data['UserId'],
        BillId=data['BillId'],
        reminder_date=data['reminder_date'],
        message=data['message']
    )
    db.session.add(new_reminder)
    db.session.commit()
    return jsonify({'message': 'Reminder created', 'ReminderId': new_reminder.ReminderId}), 201

@auth_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    # Update reminder
    reminder = Reminder.query.get_or_404(reminder_id)
    data = request.json
    
    reminder.UserId = data.get('UserId', reminder.UserId)
    reminder.BillId = data.get('BillId', reminder.BillId)
    reminder.reminder_date = data.get('reminder_date', reminder.reminder_date)
    reminder.message = data.get('message', reminder.message)
    
    db.session.commit()
    return jsonify({'message': 'Reminder updated'}), 200

@auth_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    # Delete reminder
    reminder = Reminder.query.get_or_404(reminder_id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'message': 'Reminder deleted'}), 200
