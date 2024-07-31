from flask import Blueprint, request, jsonify
from models import Notification
from models import db

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['GET'])
def get_notifications():
    # Retrieve all notifications
    pass

@notifications_bp.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    # Retrieve specific notification
    pass

@notifications_bp.route('/notifications', methods=['POST'])
def create_notification():
    # Create new notification
    pass

@notifications_bp.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    # Update notification
    pass

@notifications_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    # Delete notification
    pass
