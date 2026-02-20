from flask import Flask, jsonify, request

from db import db

from models.categories import Categories
from models.products import Products
from models.companies import Companies


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
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400
  
  query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

  values['category_id'] = query.category_id

  return jsonify({"message": "category created", "result": values}), 201

def get_all_categories():
  companies = db.session.query(Categories).all()

  company_list = []

  for company in companies:
    company_record = {
      "company_id": company.company_id,
      "company_name": company.company_name
    }

  company_list.append(company_record)


def category_by_id(category_id):
  if request.method == 'GET':
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category:
      return jsonify({"message": f"category {category_id} does not exist"}), 400
      
    record = {
      'category_id' : category.category_id,
      'category_name' : category.category_name
    }

    return jsonify({"message": "product found", "results": record}), 200
  
  elif request.method == 'PUT':
    data = request.form if request.form else request.get_json()
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    category.category_name = data.get("category_name", category.category_name)

    try:
      db.session.commit()
    except:
      db.session.rollback()
      return jsonify({"message": "unable to update record"}), 400
    
    updated_category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    category = {
      'category_id': updated_category.category_id,
      'category_name': updated_category.category_name
    }
    
    return jsonify({"message": "category updated", "results": category}), 200

def delete_category(category_id):
  category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

  if not category:
    return jsonify({"message":f"category by id {category_id} does not exist"}), 400
  
  try:
    db.session.delete(category)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete record"}), 400
  
  return jsonify({"message": "category deleted"}), 200
