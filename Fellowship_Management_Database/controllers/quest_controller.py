from flask import jsonify, request

from db import db
from models.quest import Quests, quest_schema, quests_schema, quest_details_schema
from util.reflection import populate_object


def add_quest():
  post_data = request.form if request.form else request.get_json()

  new_quest = Quests.new_quest_obj()
  populate_object(new_quest, post_data)

  try:
    db.session.add(new_quest)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create quest. {e}"}), 400
  
  return jsonify({"message": "quest created", "results": quest_schema.dump(new_quest)}), 201


def get_quests_by_difficulty(difficulty_level):
  quests_query = db.session.query(Quests).filter(Quests.difficulty_level == difficulty_level).all()

  if not quests_query:
    return jsonify({"message": "no quests found"}), 404

  return jsonify({"message": "quests found", "results": quests_schema.dump(quests_query)}), 200


def quest_by_id(quest_id):
  quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

  if not quest_query:
    return jsonify({"message": f"no quests found with id {quest_id}"}), 404
  
  if request.method == 'PUT':
    post_data = request.form if request.form else request.get_json()
    populate_object(quest_query, post_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update quest. {e}"}), 400
    
    return jsonify({"message": "quest updated", "results": quest_schema.dump(quest_query)}), 200
  
  elif request.method == 'GET':
    return jsonify({"message": "quest found", "results": quest_details_schema.dump(quest_query)}), 200


def complete_quest(quest_id):
  quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

  if not quest_query:
    return jsonify({"message": f"no quests found with id {quest_id}"}), 404
  
  patch_data = {"is_completed":True}


  populate_object(quest_query, patch_data )

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to complete quest. {e}"}), 400
    
  return jsonify({"message": "quest completed", "results": quest_schema.dump(quest_query)}), 200



def delete_quest(quest_id):
  quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

  if not quest_query:
     return jsonify({"message": f"no quests found with id {quest_id}"}), 404

  try:
    db.session.delete(quest_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete quest. {e}"}), 400
  
  return jsonify({"message": "quest deleted", "results": quest_schema.dump(quest_query)}), 200

