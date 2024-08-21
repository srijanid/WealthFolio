from flask import Blueprint, request, jsonify
from models import Budget
from models import db
import datetime

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budgets', methods=['GET'])
def get_budgets():
    # Retrieve all budgets
     budgets = Budget.query.all()
     budget_list = [{
        'BudgetId': budget.BudgetId,
        'UserID': budget.UserID,
        'CategoryId': budget.CategoryId,
        'budget_amount': str(budget.budget_amount),
        'TransactionId': budget.TransactionId,
        'Amount': str(budget.Amount),
        'description': budget.description,
        'creation_date': budget.creation_date,
        'status': budget.status,
        'amount_pending': str(budget.amount_pending),
        'UpdatedAt': budget.UpdatedAt
    } for budget in budgets]
    
     return jsonify(budget_list), 200

@budget_bp.route('/budgets/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    # Retrieve specific budget
    budget = Budget.query.get_or_404(budget_id)
    budget_data = {
        'BudgetId': budget.BudgetId,
        'UserID': budget.UserID,
        'CategoryId': budget.CategoryId,
        'budget_amount': str(budget.budget_amount),
        'TransactionId': budget.TransactionId,
        'Amount': str(budget.Amount),
        'description': budget.description,
        'creation_date': budget.creation_date,
        'status': budget.status,
        'amount_pending': str(budget.amount_pending),
        'UpdatedAt': budget.UpdatedAt
    }
    
    return jsonify(budget_data), 200

@budget_bp.route('/budgets', methods=['POST'])
def create_budget():
    # Create new budget
    data = request.json
    new_budget = Budget(
        UserID=data['UserID'],
        CategoryId=data['CategoryId'],
        budget_amount=data['budget_amount'],
        TransactionId=data.get('TransactionId'),
        Amount=data.get('Amount', 0),
        description=data.get('description'),
        status=data.get('status', 'Active'),
        amount_pending=data.get('amount_pending', 0)
    )
    
    db.session.add(new_budget)
    db.session.commit()
    
    return jsonify({'message': 'New budget created', 'BudgetId': new_budget.BudgetId}), 201

@budget_bp.route('/budgets/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    # Update budget
    budget = Budget.query.get_or_404(budget_id)
    data = request.json
    
    budget.UserID = data.get('UserID', budget.UserID)
    budget.CategoryId = data.get('CategoryId', budget.CategoryId)
    budget.budget_amount = data.get('budget_amount', budget.budget_amount)
    budget.TransactionId = data.get('TransactionId', budget.TransactionId)
    budget.Amount = data.get('Amount', budget.Amount)
    budget.description = data.get('description', budget.description)
    budget.status = data.get('status', budget.status)
    budget.amount_pending = data.get('amount_pending', budget.amount_pending)
    
    db.session.commit()
    
    return jsonify({'message': 'Budget updated'}), 200

@budget_bp.route('/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    # Delete budget
    budget = Budget.query.get_or_404(budget_id)
    
    db.session.delete(budget)
    db.session.commit()
    
    return jsonify({'message': 'Budget deleted'}), 200
