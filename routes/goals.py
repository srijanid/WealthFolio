from flask import Blueprint, request, jsonify
from models import Goal
from models import db

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/goals', methods=['GET'])
def get_goals():
    # Retrieve all goals
    pass

@goals_bp.route('/goals/<int:goal_id>', methods=['GET'])
def get_goal(goal_id):
    # Retrieve specific goal
    pass

@goals_bp.route('/goals', methods=['POST'])
def create_goal():
    # Create new goal
    pass

@goals_bp.route('/goals/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    # Update goal
    pass

@goals_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    # Delete goal
    pass
