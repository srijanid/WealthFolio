from flask import Blueprint, request, jsonify
from models import Receipt
from models import db
from . import auth_bp

#receipts_bp = Blueprint('receipts', __name__)

@auth_bp.route('/receipts', methods=['GET'])
# Retrieve all receipts for a user
def get_receipts_for_user(user_id):
    receipts = Receipt.query.filter_by(UserId=user_id).all()
    receipt_list = [{
        'ReceiptId': receipt.ReceiptId,
        'TransactionId': receipt.TransactionId,
        'UserId': receipt.UserId,
        'Amount': str(receipt.Amount),
        'ReceiptDate': receipt.ReceiptDate,
        'Description': receipt.Description,
        'CreatedAt': receipt.CreatedAt,
        'UpdatedAt': receipt.UpdatedAt
    } for receipt in receipts]
    return jsonify(receipt_list), 200

@auth_bp.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    # Retrieve specific receipt
    receipt = Receipt.query.get_or_404(receipt_id)
    receipt_data = {
        'ReceiptId': receipt.ReceiptId,
        'TransactionId': receipt.TransactionId,
        'UserId': receipt.UserId,
        'Amount': str(receipt.Amount),
        'ReceiptDate': receipt.ReceiptDate,
        'Description': receipt.Description,
        'CreatedAt': receipt.CreatedAt,
        'UpdatedAt': receipt.UpdatedAt
    }
    return jsonify(receipt_data), 200

@auth_bp.route('/receipts', methods=['POST'])
def create_receipt():
    # Create new receipt
    data = request.json
    new_receipt = Receipt(
        TransactionId=data['TransactionId'],
        UserId=data['UserId'],
        Amount=data['Amount'],
        ReceiptDate=data['ReceiptDate'],
        Description=data.get('Description')
    )
    db.session.add(new_receipt)
    db.session.commit()
    return jsonify({'message': 'Receipt created', 'ReceiptId': new_receipt.ReceiptId}), 201

@auth_bp.route('/receipts/<int:receipt_id>', methods=['PUT'])
def update_receipt(receipt_id):
    # Update receipt
    receipt = Receipt.query.get_or_404(receipt_id)
    data = request.json
    
    receipt.TransactionId = data.get('TransactionId', receipt.TransactionId)
    receipt.UserId = data.get('UserId', receipt.UserId)
    receipt.Amount = data.get('Amount', receipt.Amount)
    receipt.ReceiptDate = data.get('ReceiptDate', receipt.ReceiptDate)
    receipt.Description = data.get('Description', receipt.Description)
    
    db.session.commit()
    return jsonify({'message': 'Receipt updated'}), 200

@auth_bp.route('/receipts/<int:receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    # Delete receipt
    receipt = Receipt.query.get_or_404(receipt_id)
    db.session.delete(receipt)
    db.session.commit()
    return jsonify({'message': 'Receipt deleted'}), 200
