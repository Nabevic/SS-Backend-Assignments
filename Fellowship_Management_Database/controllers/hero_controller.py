from flask import jsonify, request

from db import db
from models.hero import Heroes, hero_schema, heroes_schema
from models.quest import Quests, quest_schema, quests_schema
from util.reflection import populate_object


def add_hero():
  post_data = request.form if request.form else request.get_json()

  new_hero = Heroes.new_hero_obj()
  populate_object(new_hero, post_data)

  try:
    db.session.add(new_hero)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create hero. {e}"}), 400
  
  return jsonify({"message": "hero created", "results": hero_schema.dump(new_hero)}), 201


def add_hero_quest(): #double check logic
  post_data = request.form if request.form else request.get_json()
  hero_query = db.session.query(Heroes).filter(Heroes.hero_id == post_data['hero_id']).first()
  quest_query = db.session.query(Quests).filter(Quests.quest_id == post_data['quest_id']).first()


  if not hero_query:
    return jsonify({"message":f"no heroes found with id {post_data['hero_id']}"}), 404
  
  elif not quest_query:
    return jsonify({"message":f"no heroes found with id {post_data['quest_id']}"}), 404

  if hero_query and quest_query:
    hero_query.quests.append(quest_query)
    db.session.commit()

  return jsonify({"message": "quest added to hero", "result": hero_schema.dump(hero_query)}), 201


def get_heroes():
  heroes_query = db.session.query(Heroes).all()

  if not heroes_query:
    return jsonify({"message": "no heroes found"}), 404

  return jsonify({"message": "heroes found", "results": heroes_schema.dump(heroes_query)}), 200


def get_heroes_alive():
  heroes_query = db.session.query(Heroes).filter(Heroes.is_alive == True).all()

  if not heroes_query:
    return jsonify({"message": "no heroes found"}), 404

  return jsonify({"message": "heroes found", "results": heroes_schema.dump(heroes_query)}), 200


def get_hero_quests(hero_id): #double check logic
  quest_query = db.session.query(Quests).join('HeroesQuestsAssociation').join(Heroes).filter(Heroes.hero_id == hero_id).all()
  if not quest_query:
    return jsonify({"message": "no quests found"}), 404
  
  return jsonify({"message": "quests found", "results": quests_schema.dump(quest_query)}), 200


def hero_by_id(hero_id):
  hero_query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

  if not hero_query:
    return jsonify({"message": f"no heroes found with id {hero_id}"}), 404
  
  if request.method == 'PUT':
    post_data = request.form if request.form else request.get_json()
    populate_object(hero_query, post_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update hero. {e}"}), 400
    
    return jsonify({"message": "hero updated", "results": hero_schema.dump(hero_query)}), 200
  
  elif request.method == 'GET':
    return jsonify({"message": "hero found", "results": hero_schema.dump(hero_query)}), 200
  

def delete_hero(hero_id):
  hero_query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

  if not hero_query:
     return jsonify({"message": f"no heroes found with id {hero_id}"}), 404

  try:
    db.session.delete(hero_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete hero. {e}"}), 400
  
  return jsonify({"message": "hero deleted", "results": hero_schema.dump(hero_query)}), 200
