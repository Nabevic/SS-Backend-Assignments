from flask import jsonify, request

from db import db
from models.ability import Abilities, ability_schema, abilities_schema
from util.reflection import populate_object

def add_ability():
  post_data = request.form if request.form else request.get_json()

  new_ability = Abilities.new_ability_obj()
  populate_object(new_ability, post_data)

  try:
    db.session.add(new_ability)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create ability. {e}"}), 400
  
  return jsonify({"message": "ability created", "results": ability_schema.dump(new_ability)}), 201


def update_ability(ability_id):
  ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()
  post_data = request.form if request.form else request.get_json()

  if not ability_query:
     return jsonify({"message": f"no abilities found with id {ability_id}"}), 404
  
  populate_object(ability_query, post_data)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to update ability. {e}"}), 400
  
  return jsonify({"message": "ability updated", "results": ability_schema.dump(ability_query)}), 200


def delete_ability(ability_id):
  ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

  if not ability_query:
     return jsonify({"message": f"no abilities found with id {ability_id}"}), 404

  try:
    db.session.delete(ability_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete ability. {e}"}), 400
  
  return jsonify({"message": "ability deleted", "results": ability_schema.dump(ability_query)}), 200
