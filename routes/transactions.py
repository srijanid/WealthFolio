from flask import Blueprint, request, jsonify
from models import Transaction
from models import db

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    # Retrieve all transactions
    pass

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    # Retrieve specific transaction
    pass

@transactions_bp.route('/transactions', methods=['POST'])
def create_transaction():
    # Create new transaction
    pass

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    # Update transaction
    pass

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    # Delete transaction
    pass
