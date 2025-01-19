from flask import Blueprint, request, jsonify
from models import Goal, db
from . import auth_bp

#goals_bp = Blueprint('goals', __name__)

@auth_bp.route('/goals', methods=['GET'])
def get_goals():
    # Retrieve all goals from the database
    try:
        goals = Goal.query.all()
        return jsonify([goal.to_dict() for goal in goals])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/goals/<int:goal_id>', methods=['GET'])
def get_goal(goal_id):
    # Retrieve specific goal by ID from the database
    try:
        goal = Goal.query.get(goal_id)
        if goal is None:
            return jsonify({"error": "Goal not found"}), 404
        return jsonify(goal.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/goals', methods=['POST'])
def create_goal():
    # Create a new goal and save it to the database
    data = request.json
    try:
        new_goal = Goal(
            UserId=data.get('UserId'),
            goal_name=data.get('goal_name'),
            target_amount=data.get('target_amount'),
            saved_amount=data.get('saved_amount', 0),
            target_date=data.get('target_date')
        )
        db.session.add(new_goal)
        db.session.commit()
        return jsonify(new_goal.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/goals/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    # Update an existing goal by ID
    data = request.json
    try:
        goal = Goal.query.get(goal_id)
        if goal is None:
            return jsonify({"error": "Goal not found"}), 404

        goal.goal_name = data.get('goal_name', goal.goal_name)
        goal.target_amount = data.get('target_amount', goal.target_amount)
        goal.saved_amount = data.get('saved_amount', goal.saved_amount)
        goal.target_date = data.get('target_date', goal.target_date)
        
        db.session.commit()
        return jsonify(goal.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    # Delete a specific goal by ID
    try:
        goal = Goal.query.get(goal_id)
        if goal is None:
            return jsonify({"error": "Goal not found"}), 404

        db.session.delete(goal)
        db.session.commit()
        return jsonify({"message": "Goal deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Helper method to convert Goal model to dictionary
def goal_to_dict(self):
    return {
        "GoalId": self.GoalId,
        "UserId": self.UserId,
        "goal_name": self.goal_name,
        "target_amount": float(self.target_amount),
        "saved_amount": float(self.saved_amount),
        "target_date": self.target_date.isoformat(),
        "CreatedAt": self.CreatedAt.isoformat(),
        "UpdatedAt": self.UpdatedAt.isoformat()
    }

# Add the to_dict method to the Goal model
Goal.to_dict = goal_to_dict

