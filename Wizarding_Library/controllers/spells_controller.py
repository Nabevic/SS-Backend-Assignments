from flask import Flask, jsonify, request

from db import db
from models.spells import Spells

def construct_record(query):
  spell_record = {
    "spell_id": query.spell_id,
    "spell_name": query.spell_name,
    "incantation": query.incantation,
    "difficulty_level": query.difficulty_level,
    "spell_type": query.spell_type,
    "description": query.description
  }
  return spell_record


def add_spell():
  post_data = request.form if request.form else request.get_json()

  fields = ["spell_name", "incantation", "difficulty_level", "spell_type", "description"]
  required_fields = ['spell_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message": f'{field} is required'}), 400
    values[field] = field_data
  
  new_spell = Spells(**values)

  try:
    db.session.add(new_spell)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400 
  
  query = db.session.query(Spells).filter(Spells.spell_name == values['spell_name']).first()
  spell_record = construct_record(query)

  return jsonify({"message": "book created", "result": spell_record}), 201


def get_spells():
  spells_query = db.session.query(Spells).all()
  if not spells_query:
    return jsonify({"message": "no spells found"}), 404

  spell_list = []
  for spell in spells_query:
    spell_record = construct_record(spell)
    spell_list.append(spell_record)

  return jsonify({"message": "spells found", "result": spell_list})


def get_spells_by_difficulty(difficulty_level):
  spells_query = db.session.query(Spells).filter(Spells.difficulty_level == difficulty_level).all()
  if not spells_query:
    return jsonify({"message": f"no products found with difficulty_level {difficulty_level}"}), 404
  
  else:
    spell_list = []

  for spell in spells_query:
    spell_record = construct_record(spell)
    spell_list.append(spell_record)

  return jsonify({"message": "spells found", "result": spell_list}), 200


def update_spell(spell_id):
  data = request.form if request.form else request.get_json()
  spell_query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

  if not spell_query:
    return jsonify({"message": f"spell not found with id {spell_id}"}), 404 

  spell_query.spell_name = data.get("spell_name", spell_query.spell_name)
  spell_query.incantation = data.get("incantation", spell_query.incantation)
  spell_query.difficulty_level = data.get("difficulty_level", spell_query.difficulty_level)
  spell_query.spell_type = data.get("spell_type", spell_query.spell_type)
  spell_query.description = data.get("description", spell_query.description)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message:": f"unable to update record: {e}"}), 400
  
  updated_spell = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()
  spell_record = construct_record(updated_spell)

  return jsonify({"message": "spell updated", "results": spell_record}), 200


def delete_spell(spell_id):
  spell_query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

  if not spell_query:
    return jsonify({"message": f"spell not found with id {spell_id}"}), 404

  deleted_record = construct_record(spell_query)

  try:
    db.session.delete(spell_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message":f"unable to delete spell. {e}"}), 400
  
  return jsonify({"message": "spell deleted","results": deleted_record})