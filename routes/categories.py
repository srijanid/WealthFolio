from flask import Blueprint, request, jsonify
from models import Category, db


categories_bp = Blueprint('categories', __name__)

# Route to create a new category
@categories_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category_name = data.get('category_name')
    description = data.get('description')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    new_category = Category(category_name=category_name, Description=description)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "CategoryId": new_category.CategoryId,
        "category_name": new_category.category_name,
        "description": new_category.Description,
        "CreatedAt": new_category.CreatedAt,
        "UpdatedAt": new_category.UpdatedAt
    }), 201

# Route to get all categories
@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        "CategoryId": category.CategoryId,
        "category_name": category.category_name,
        "description": category.Description,
        "CreatedAt": category.CreatedAt,
        "UpdatedAt": category.UpdatedAt
    } for category in categories])

# Route to get a category by its ID
@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({
        "CategoryId": category.CategoryId,
        "category_name": category.category_name,
        "description": category.Description,
        "CreatedAt": category.CreatedAt,
        "UpdatedAt": category.UpdatedAt
    })

# Route to update an existing category
@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    data = request.get_json()
    category_name = data.get('category_name')
    description = data.get('description')

    if category_name:
        category.category_name = category_name
    if description:
        category.Description = description

    db.session.commit()

    return jsonify({
        "CategoryId": category.CategoryId,
        "category_name": category.category_name,
        "description": category.Description,
        "CreatedAt": category.CreatedAt,
        "UpdatedAt": category.UpdatedAt
    })

# Route to delete a category
@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200
