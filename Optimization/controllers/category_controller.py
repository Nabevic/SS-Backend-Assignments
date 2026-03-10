from flask import jsonify, request

from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object
from db import db


def add_category():
  post_data = request.form if request.form else request.get_json()

  new_category = Categories.new_category_obj()
  populate_object(new_category, post_data)

  try:
    db.session.add(new_category)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create category. {e}"}), 400

  return jsonify({"message": "category created","result": category_schema.dump(new_category)}), 201

def get_all_categories():
  categories_query = db.session.query(Categories).all()

  return jsonify({"message": "categories retrieved", "result": categories_schema.dump(categories_query)}), 200


def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:      
        return jsonify({"message": "record not found"}), 404
    
    return jsonify({"message": "category retrieved", "results": category_schema.dump(category_query)}), 200


def update_category(category_id):
  post_data = request.form if request.form else request.get_json()
  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

  if not category_query:
    return jsonify({"message": "category not found"}), 404
  
  populate_object(category_query, post_data)
  db.session.commit()

  return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200

def delete_category(category_id):
  category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

  if not category_query:
    return jsonify({"message":f"category by id {category_id} not found"}), 400
  
  try:
    db.session.delete(category_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  return jsonify({"message": "category deleted", "result": category_schema.dump(category_query)}), 200

