from flask import Blueprint, request, jsonify
from models import Transaction, Category
from models import db
from . import auth_bp

#transactions_bp = Blueprint('transactions', __name__)

@auth_bp.route('/transactions', methods=['GET'])
def get_transactions_for_user(user_id):
    # Retrieve all transactions for a user
    transactions = Transaction.query.filter_by(UserId=user_id).all()
    transaction_list = [{
        'TransactionId': transaction.TransactionId,
        'UserId': transaction.UserId,
        'CategoryId': transaction.CategoryId,
        'Amount': str(transaction.Amount),
        'TransactionDate': transaction.TransactionDate,
        'Description': transaction.Description,
        'CreatedAt': transaction.CreatedAt,
        'UpdatedAt': transaction.UpdatedAt
    } for transaction in transactions]
    return jsonify(transaction_list), 200

@auth_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    # Retrieve specific transaction by ID
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction_data = {
        'TransactionId': transaction.TransactionId,
        'UserId': transaction.UserId,
        'CategoryId': transaction.CategoryId,
        'Amount': str(transaction.Amount),
        'TransactionDate': transaction.TransactionDate,
        'Description': transaction.Description,
        'CreatedAt': transaction.CreatedAt,
        'UpdatedAt': transaction.UpdatedAt
    }
    return jsonify(transaction_data), 200

@auth_bp.route('/transactions', methods=['POST'])
def create_transaction():
    # Create new transaction
    data = request.json
    new_transaction = Transaction(
        UserId=data['UserId'],
        CategoryId=data['CategoryId'],
        Amount=data['Amount'],
        TransactionDate=data['TransactionDate'],
        Description=data.get('Description')
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created', 'TransactionId': new_transaction.TransactionId}), 201

@auth_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    # Update transaction
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.json
    
    transaction.UserId = data.get('UserId', transaction.UserId)
    transaction.CategoryId = data.get('CategoryId', transaction.CategoryId)
    transaction.Amount = data.get('Amount', transaction.Amount)
    transaction.TransactionDate = data.get('TransactionDate', transaction.TransactionDate)
    transaction.Description = data.get('Description', transaction.Description)
    
    db.session.commit()
    return jsonify({'message': 'Transaction updated'}), 200

@auth_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    # Delete transaction
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted'}), 200
