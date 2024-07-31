from flask import Blueprint, request, jsonify
from models import BillPayment
from models import db

bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/bills', methods=['GET'])
def get_bills():
    # Retrieve all bills
    pass

@bill_bp.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    # Retrieve specific bill
    pass

@bill_bp.route('/bills', methods=['POST'])
def create_bill():
    # Create new bill
    pass

@bill_bp.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    # Update bill
    pass

@bill_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    # Delete bill
    pass
