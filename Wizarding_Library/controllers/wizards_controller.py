from flask import Flask, jsonify, request

from db import db
from models.wizards import Wizards
from models.spells import Spells

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
  
  wizard_query = db.session.query(Wizards).filter(Wizards.wizard_id == values['wizard_id']).first()
  spell_query = db.session.query(Spells).filter(Spells.spell_id == values['spell_id']).first()

  if not wizard_query:
    return jsonify({"message":"wizard id does not exist"}), 404
  
  elif not spell_query:
    return jsonify({"message":"spell id does not exist"}), 404

  if wizard_query and spell_query:

    try:
      wizard_query.spells.append(spell_query)
      db.session.commit()

    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"could not add specialization. {e}"}), 400

    spells_list = []
    
    for spell in wizard_query.spells:
      spells_list.append({
        "spell_id": spell.spell_id,
        "spell_name": spell.spell_name,
        "incantation": spell.incantation,
        "difficulty_level": spell.difficulty_level,
        "spell_type": spell.spell_type,
        "description": spell.description,

      })

    wizard = {
      "wizard_id": wizard_query.wizard_id,
      "school_id": wizard_query.school_id,
      "wizard_name": wizard_query.wizard_name,
      "house": wizard_query.house,
      "year_enrolled": wizard_query.year_enrolled,
      "magical_power_level": wizard_query.magical_power_level,
      "active": wizard_query.active,
      'spells': spells_list
    }

  return jsonify({"message": "spell added to wizard", "result": wizard}), 201


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
