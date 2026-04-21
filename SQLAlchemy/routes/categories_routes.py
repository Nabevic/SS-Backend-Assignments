from flask import Blueprint
import controllers


category = Blueprint('category', __name__)

@category.route('/category', methods=['Post'])
def add_category():
  return controllers.add_category()

@category.route('/categories', methods=['GET'])
def get_all_categories():
  return controllers.get_all_categories()

@category.route('/category/<category_id>', methods=['GET','PUT'])
def category_by_id(category_id):
  return controllers.category_by_id(category_id)

@category.route('/category/delete', methods=['DELETE'])
def delete_category():
  return controllers.delete_category()