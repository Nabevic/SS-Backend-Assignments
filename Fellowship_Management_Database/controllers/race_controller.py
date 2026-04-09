from flask import jsonify, request

from db import db
from models.race import Races, race_schema, races_schema, race_details_schema
from util.reflection import populate_object





def add_race():
  post_data = request.form if request.form else request.get_json()

  new_race = Races.new_race_obj()
  populate_object(new_race, post_data)

  try:
    db.session.add(new_race)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create race. {e}"}), 400
  
  return jsonify({"message": "race created", "results": race_schema.dump(new_race)}), 201


def get_races():
  races_query = db.session.query(Races).all()

  if not races_query:
    return jsonify({"message": "no races found"}), 404

  return jsonify({"message": "races found", "results": races_schema.dump(races_query)}), 200


def race_by_id(race_id):
  race_query = db.session.query(Races).filter(Races.race_id == race_id).first()

  if not race_query:
    return jsonify({"message": f"no races found with id {race_id}"}), 404
  
  if request.method == 'PUT':
    post_data = request.form if request.form else request.get_json()
    populate_object(race_query, post_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update race. {e}"}), 400
    
    return jsonify({"message": "race updated", "results": race_schema.dump(race_query)}), 200
  
  elif request.method == 'GET':
    return jsonify({"message": "race found", "results": race_details_schema.dump(race_query)}), 200


def delete_race(race_id):
  race_query = db.session.query(Races).filter(Races.race_id == race_id).first()

  if not race_query:
     return jsonify({"message": f"no races found with id {race_id}"}), 404

  try:
    db.session.delete(race_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete race. {e}"}), 400
  
  return jsonify({"message": "race deleted", "results": race_schema.dump(race_query)}), 200
