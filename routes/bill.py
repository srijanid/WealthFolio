from flask import Blueprint, request, jsonify
from models import BillPayment
from models import db

bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/bills', methods=['GET'])
def get_bill_payments_for_user(user_id):
    # Retrieve all bill payments for a user
    bill_payments = BillPayment.query.filter_by(UserId=user_id).all()
    bill_payment_list = [{
        'BillId': bill_payment.BillId,
        'UserId': bill_payment.UserId,
        'TransactionId': bill_payment.TransactionId,
        'Amount': str(bill_payment.Amount),
        'Due_date': bill_payment.Due_date,
        'Paid_date': bill_payment.Paid_date,
        'Description': bill_payment.Description,
        'status': bill_payment.status,
        'CreatedAt': bill_payment.CreatedAt,
        'UpdatedAt': bill_payment.UpdatedAt
    } for bill_payment in bill_payments]
    return jsonify(bill_payment_list), 200

@bill_bp.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    # Retrieve specific bill
    bill_payment = BillPayment.query.get_or_404(bill_id)
    bill_payment_data = {
        'BillId': bill_payment.BillId,
        'UserId': bill_payment.UserId,
        'TransactionId': bill_payment.TransactionId,
        'Amount': str(bill_payment.Amount),
        'Due_date': bill_payment.Due_date,
        'Paid_date': bill_payment.Paid_date,
        'Description': bill_payment.Description,
        'status': bill_payment.status,
        'CreatedAt': bill_payment.CreatedAt,
        'UpdatedAt': bill_payment.UpdatedAt
    }
    return jsonify(bill_payment_data), 200

@bill_bp.route('/bills', methods=['POST'])
def create_bill():
    # Create new bill
    data = request.json
    new_bill_payment = BillPayment(
        UserId=data['UserId'],
        TransactionId=data['TransactionId'],
        Amount=data['Amount'],
        Due_date=data['Due_date'],
        Paid_date=data.get('Paid_date'),
        Description=data.get('Description'),
        status=data.get('status', 'Unpaid')
    )
    db.session.add(new_bill_payment)
    db.session.commit()
    return jsonify({'message': 'Bill payment created', 'BillId': new_bill_payment.BillId}), 201

@bill_bp.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    # Update bill
    bill_payment = BillPayment.query.get_or_404(bill_id)
    data = request.json
    
    bill_payment.UserId = data.get('UserId', bill_payment.UserId)
    bill_payment.TransactionId = data.get('TransactionId', bill_payment.TransactionId)
    bill_payment.Amount = data.get('Amount', bill_payment.Amount)
    bill_payment.Due_date = data.get('Due_date', bill_payment.Due_date)
    bill_payment.Paid_date = data.get('Paid_date', bill_payment.Paid_date)
    bill_payment.Description = data.get('Description', bill_payment.Description)
    bill_payment.status = data.get('status', bill_payment.status)
    
    db.session.commit()
    return jsonify({'message': 'Bill payment updated'}), 200

@bill_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    # Delete bill
    bill_payment = BillPayment.query.get_or_404(bill_id)
    db.session.delete(bill_payment)
    db.session.commit()
    return jsonify({'message': 'Bill payment deleted'}), 200
