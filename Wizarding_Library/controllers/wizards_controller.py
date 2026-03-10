from flask import Flask, jsonify, request

from db import db
from models.wizards import Wizards

def construct_record(query):
  wizard_record = {
    "wizard_id": query.wizard_id,
    "school_id": query.school_id,
    "wizard_name": query.wizard_name,
    "house": query.house,
    "year_enrolled": query.year_enrolled,
    "magical_power_level": query.magical_power_level,
    "active": query.active
  }
  return wizard_record



def add_wizard():
  post_data = request.form if request.form else request.get_json()

  fields = ["school_id", "wizard_name", "house", "year_enrolled", "magical_power_level", "active"]
  required_fields = ['school_id','wizard_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message": f'{field} is required'}), 400
    values[field] = field_data
  
  new_wizard = Wizards(**values)

  try:
    db.session.add(new_wizard)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400 
  
  query = db.session.query(Wizards).filter(Wizards.wizard_name == values['wizard_name']).first()
  wizard_record = construct_record(query)

  return jsonify({"message": "wizard created", "result": wizard_record}), 201


def add_wizard_specialization():
  post_data = request.form if request.form else request.get_json()

  fields = ['wizard_id','spell_id', "proficiency_level", "date_learned"]
  required_fields = ['wizard_id','spell_id']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message":f"{field} is required"}), 400
    values[field] = field_data
  
  product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
  category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

  if not product_query:
    return jsonify({"message":"product id does not exist"}), 404
  
  elif not category_query:
    return jsonify({"message":"category id does not exist"}), 404

  if product_query and category_query:

    try:
      product_query.categories.append(category_query)
      db.session.commit()

    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"could not add association. {e}"}), 400

    categories_list = []
    
    for category in product_query.categories:
      categories_list.append({
        "category_id": category.category_id,
        "category_name": category.category_name
      })

    company_dict = {
      "company_id": product_query.companies.company_id,
      "category_name": product_query.companies.company_name
    }
    product = {
      'product_id': product_query.product_id,
      'product_name': product_query.product_name,
      'description': product_query.description,
      'price': product_query.price,
      'active': product_query.active,
      'company': company_dict,
      'categories': categories_list,
    }

  return jsonify({"message": "category added to product", "result": product}), 201


def get_all_wizards():
  wizards_query = db.session.query(Wizards).all()
  if not wizards_query:
    return jsonify({"message": "no wizards found"}), 404

  wizard_list = []
  for wizard in wizards_query:
    wizard_record = construct_record(wizard)
    wizard_list.append(wizard_record)

  return jsonify({"message": "wizards found", "result": wizard_list})


def get_active_wizards():
  wizards_query = db.session.query(Wizards).filter(Wizards.active == True).all()

  wizard_list = []
  for wizard in wizards_query:
    wizard_record = construct_record(wizard)
    wizard_list.append(wizard_record)

  return jsonify({"message": "wizards found", "result": wizard_list})


def get_wizards_by_house(house):
  wizards_query = db.session.query(Wizards).filter(Wizards.house == house).all()
  if not wizards_query:
    return jsonify({"message": f"no products found with house {house}"}), 404
  
  else:
    wizard_list = []

  for wizard in wizards_query:
    wizard_record = construct_record(wizard)
    wizard_list.append(wizard_record)

  return jsonify({"message": "wizards found", "result": wizard_list}), 200


def get_wizards_by_power(magical_power_level):
  wizards_query = db.session.query(Wizards).filter(Wizards.magical_power_level == magical_power_level).all()
  if not wizards_query:
    return jsonify({"message": f"no products found with magical power level {magical_power_level}"}), 404
  
  else:
    wizard_list = []

  for wizard in wizards_query:
    wizard_record = construct_record(wizard)
    wizard_list.append(wizard_record)

  return jsonify({"message": "wizards found", "result": wizard_list}), 200


def wizard_id(wizard_id):
  wizard_query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

  if not wizard_query:
    return jsonify({"message": f"wizard not found with id {wizard_id}"}), 404 
  
  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()

    wizard_query.school_id = data.get("school_id", wizard_query.school_id)
    wizard_query.wizard_name = data.get("wizard_name", wizard_query.wizard_name)
    wizard_query.house = data.get("house", wizard_query.house)
    wizard_query.year_enrolled = data.get("year_enrolled", wizard_query.year_enrolled)
    wizard_query.magical_power_level = data.get("magical_power_level", wizard_query.magical_power_level)
    wizard_query.active = data.get("active", wizard_query.active)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message:": f"unable to update record: {e}"}), 400
    
    updated_wizard = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()
    wizard_record = construct_record(updated_wizard)

    return jsonify({"message": "wizard updated", "results": wizard_record}), 200
  
  elif request.method == 'GET':
    wizard_record = construct_record(wizard_query)

    return jsonify({"message": "school found", "result": wizard_record}), 200


def delete_wizard(wizard_id):
  wizard_query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

  if not wizard_query:
    return jsonify({"message": f"wizard not found with id {wizard_id}"}), 404

  deleted_record = construct_record(wizard_query)

  try:
    db.session.delete(wizard_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message":f"unable to delete wizard. {e}"}), 400
  
  return jsonify({"message": "wizard deleted","results": deleted_record})
