from flask import Blueprint, request, jsonify
from models import Receipt
from models import db

receipts_bp = Blueprint('receipts', __name__)

@receipts_bp.route('/receipts', methods=['GET'])
def get_receipts():
    # Retrieve all receipts
    pass

@receipts_bp.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    # Retrieve specific receipt
    pass

@receipts_bp.route('/receipts', methods=['POST'])
def create_receipt():
    # Create new receipt
    pass

@receipts_bp.route('/receipts/<int:receipt_id>', methods=['PUT'])
def update_receipt(receipt_id):
    # Update receipt
    pass

@receipts_bp.route('/receipts/<int:receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    # Delete receipt
    pass
