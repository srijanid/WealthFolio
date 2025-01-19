from flask import Blueprint, request, jsonify
from models import Category
from models import db
from . import auth_bp

@auth_bp.route('/categories', methods=['GET'])
@auth_bp.route('/categories/user/<int:user_id>', methods=['GET'])
def get_categories_for_user(user_id=None):
    # Retrieve all categories or categories for a specific user
    query = Category.query
    if user_id:
        query = query.filter_by(UserID=user_id)
    categories = query.all()
    category_list = [{
        'CategoryId': category.CategoryId,
        'UserID': category.UserID,
        'category_name': category.category_name,
        'description': category.Description,
        'CreatedAt': category.CreatedAt,
        'UpdatedAt': category.UpdatedAt
    } for category in categories]
    return jsonify(category_list), 200

@auth_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    # Retrieve specific category by ID
    category = Category.query.get_or_404(category_id)
    category_data = {
        'CategoryId': category.CategoryId,
        'UserID': category.UserID,
        'category_name': category.category_name,
        'description': category.Description,
        'CreatedAt': category.CreatedAt,
        'UpdatedAt': category.UpdatedAt
    }
    return jsonify(category_data), 200

@auth_bp.route('/categories', methods=['POST'])
def create_category():
    # Create a new category
    data = request.json
    category_name = data.get('category_name')
    description = data.get('description')
    user_id = data.get('UserID')

    if not category_name or not user_id:
        return jsonify({"error": "Category name and UserID are required"}), 400

    # Check for duplicate category name for the user
    if Category.query.filter_by(category_name=category_name, UserID=user_id).first():
        return jsonify({"error": "Category name already exists for this user"}), 409

    new_category = Category(
        UserID=user_id,
        category_name=category_name,
        Description=description
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'CategoryId': new_category.CategoryId}), 201

@auth_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    # Update an existing category
    category = Category.query.get_or_404(category_id)
    data = request.json
    category_name = data.get('category_name')
    description = data.get('description')

    if category_name:
        # Ensure no duplicate category name for this user
        existing_category = Category.query.filter_by(category_name=category_name, UserID=category.UserID).first()
        if existing_category and existing_category.CategoryId != category_id:
            return jsonify({"error": "Category name already exists for this user"}), 409
        category.category_name = category_name

    if description:
        category.Description = description

    db.session.commit()
    return jsonify({'message': 'Category updated'}), 200

@auth_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    # Delete a category
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200
