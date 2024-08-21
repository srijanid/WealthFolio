from flask import Blueprint, request, jsonify
from models import Goal

budget_check_bp = Blueprint('budget_check', __name__)

@budget_check_bp.route('/check_goals', methods=['POST'])
def check_goals_within_budget():
    # Get the budget from the user input
    data = request.json
    user_budget = float(data.get('budget', 0))
    
    # Retrieve all goals from the database
    try:
        goals = Goal.query.all()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch goals from database: {str(e)}"}), 500

    results = []
    
    for goal in goals:
        goal_name = goal.goal_name
        target_amount = float(goal.target_amount)
        saved_amount = float(goal.saved_amount)
        
        # Determine the status based on the budget
        if target_amount <= user_budget and saved_amount <= user_budget:
            status = "Within Budget"
        elif abs(target_amount - user_budget) <= 500 or abs(saved_amount - user_budget) <= 500:
            status = "Yellow Alert"
        elif abs(target_amount - user_budget) <= 1000 or abs(saved_amount - user_budget) <= 1000:
            status = "Yellow Alert"
        else:
            status = "Exceeds Budget"
        
        results.append({
            "goal_name": goal_name,
            "target_amount": target_amount,
            "saved_amount": saved_amount,
            "budget": user_budget,
            "status": status
        })
    
    return jsonify(results)
