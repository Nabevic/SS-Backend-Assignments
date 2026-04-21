from flask import Flask, jsonify, request

from db import db
from models.categories import Categories

def construct_record(query):
   category_record = {
    "category_id": query.category_id,
    "category_name": query.category_name
  }
   return category_record


def add_category():
  post_data = request.form if request.form else request.get_json()

  fields = ['category_name']
  required_fields = ['category_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message":f'{field} is required'}), 400
    
    values[field] = field_data

  new_category = Categories(values['category_name'])

  try:
    db.session.add(new_category)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400
  
  query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()
  category_record = construct_record(query)

  return jsonify({"message": "category created", "result": category_record}), 201


def get_all_categories():
  categories = db.session.query(Categories).all()

  category_list = []

  for category in categories:
    category_record = construct_record(category)
    category_list.append(category_record)

  return jsonify({"message": "categories found","results": category_list})


def category_by_id(category_id):
  category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
  if not category:
    return jsonify({"message": f"category {category_id} does not exist"}), 400
  

  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()
    category.category_name = data.get("category_name", category.category_name)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update record. {e}"}), 400
    
    updated_category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    category_record = construct_record(updated_category)
    
    return jsonify({"message": "category updated", "results": category_record}), 200
  

  elif request.method == 'GET':
    category_record = construct_record(category)

    return jsonify({"message": "category found", "results": category_record}), 200


def delete_category():
  post_data = request.form if request.form else request.get_json()

  category = db.session.query(Categories).filter(Categories.category_id == post_data['category_id']).first()

  if not category:
    return jsonify({"message":f"category by id {post_data['category_id']} does not exist"}), 400
  
  else: 
    deleted_record = construct_record(category)

  try:
    db.session.delete(category)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  return jsonify({"message": "category deleted", "result": deleted_record}), 200
