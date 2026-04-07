from flask import jsonify, request

from db import db
from models.lightsabers import Lightsabers, lightsaber_schema, lightsabers_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object



@authenticate_return_auth
def add_lightsaber(auth_info):
  if auth_info.user.role =='admin':
    post_data = request.form if request.form else request.get_json()

    new_lightsaber = Lightsabers.new_lightsaber_obj()
    populate_object(new_lightsaber, post_data)
    try:
      db.session.add(new_lightsaber)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add lightsaber. {e}"}), 400
    
    return jsonify({"message": "lightsaber added", "result": lightsaber_schema.dump(new_lightsaber)}), 201
  return jsonify({"message": "unauthorized"}), 401


def get_lightsaber(owner_id):
  lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.owner_id == owner_id).first()

  if not lightsaber_query:
     return jsonify({"message": f"no lightsaber found for owner id {owner_id}"}), 404
  
  return jsonify({"message": "lightsaber found", "result": lightsaber_schema.dump(lightsaber_query)}), 200

@authenticate_return_auth #Owner only
def update_lightsaber(lightsaber_id, auth_info):
  if auth_info.user.role =='admin':
    lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.lightsaber_id == lightsaber_id).first()
    post_data = request.form if request.form else request.get_json()

    if not lightsaber_query:
     return jsonify({"message": "unable to update record; record not found"}), 404
    
    populate_object(lightsaber_query, post_data)

    db.session.commit()

    return jsonify({"message": "lightsaber updated", "result":lightsaber_schema.dump(lightsaber_query)}),200
  return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth #Owner or Council+
def delete_lightsaber(lightsaber_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.lightsaber_id == lightsaber_id).first()

    if not lightsaber_query:
      return jsonify({"message": f"no lightsaber found with id {lightsaber_id}"}), 404
    try:
      db.session.delete(lightsaber_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "lightsaber deleted", "result": lightsaber_schema.dump(lightsaber_query)}), 200
  return jsonify({"message": "unauthorized"}), 401

