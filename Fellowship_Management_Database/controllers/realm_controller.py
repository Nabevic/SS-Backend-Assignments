from flask import jsonify, request

from db import db
from models.realm import Realms, realm_schema, realms_schema
from util.reflection import populate_object


def add_realm():
  post_data = request.form if request.form else request.get_json()

  new_realm = Realms.new_realm_obj()
  populate_object(new_realm, post_data)

  try:
    db.session.add(new_realm)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create realm. {e}"}), 400
  
  return jsonify({"message": "realm created", "results": realm_schema.dump(new_realm)}), 201


def realm_by_id(realm_id):
  realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

  if not realm_query:
    return jsonify({"message": f"no realms found with id {realm_id}"}), 404
  
  if request.method == 'PUT':
    post_data = request.form if request.form else request.get_json()
    populate_object(realm_query, post_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update realm. {e}"}), 400
    
    return jsonify({"message": "realm updated", "results": realm_schema.dump(realm_query)}), 200
  
  elif request.method == 'GET':
    return jsonify({"message": "realm found", "results": realm_schema.dump(realm_query)}), 200


def delete_realm(realm_id):
  realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

  if not realm_query:
     return jsonify({"message": f"no realms found with id {realm_id}"}), 404

  try:
    db.session.delete(realm_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete realm. {e}"}), 400
  
  return jsonify({"message": "realm deleted", "results": realm_schema.dump(realm_query)}), 200