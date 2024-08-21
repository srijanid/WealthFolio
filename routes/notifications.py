from flask import Blueprint, request, jsonify
from models import Notification
from models import db

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['GET'])
@notifications_bp.route('/notifications/user/<int:user_id>', methods=['GET'])
def get_notifications_for_user(user_id):
    # Retrieve all notifications for a user
    notifications = Notification.query.filter_by(UserId=user_id).all()
    notification_list = [{
        'NotificationId': notification.NotificationId,
        'UserId': notification.UserId,
        'message': notification.message,
        'is_read': notification.is_read,
        'CreatedAt': notification.CreatedAt,
        'UpdatedAt': notification.UpdatedAt
    } for notification in notifications]
    return jsonify(notification_list), 200

@notifications_bp.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    # Retrieve specific notification by ID
    notification = Notification.query.get_or_404(notification_id)
    notification_data = {
        'NotificationId': notification.NotificationId,
        'UserId': notification.UserId,
        'message': notification.message,
        'is_read': notification.is_read,
        'CreatedAt': notification.CreatedAt,
        'UpdatedAt': notification.UpdatedAt
    }
    return jsonify(notification_data), 200

@notifications_bp.route('/notifications', methods=['POST'])
def create_notification():
    # Create new notification
    data = request.json
    new_notification = Notification(
        UserId=data['UserId'],
        message=data['message'],
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({'message': 'Notification created', 'NotificationId': new_notification.NotificationId}), 201

@notifications_bp.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    # Update a notification (mark as read or update the message)
    notification = Notification.query.get_or_404(notification_id)
    data = request.json
    notification.message = data.get('message', notification.message)
    notification.is_read = data.get('is_read', notification.is_read)
    db.session.commit()
    return jsonify({'message': 'Notification updated'}), 200

@notifications_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    # Delete notification
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted'}), 200
