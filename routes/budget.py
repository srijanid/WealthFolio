from flask import Blueprint, request, jsonify
from models import Budget
from models import db

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budgets', methods=['GET'])
def get_budgets():
    # Retrieve all budgets
    pass

@budget_bp.route('/budgets/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    # Retrieve specific budget
    pass

@budget_bp.route('/budgets', methods=['POST'])
def create_budget():
    # Create new budget
    pass

@budget_bp.route('/budgets/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    # Update budget
    pass

@budget_bp.route('/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    # Delete budget
    pass
