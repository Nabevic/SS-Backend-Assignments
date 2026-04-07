from flask import jsonify, request

from db import db
from models.padawans import Padawans, padawan_schema, padawans_schema
from models.users import Users, user_schema, users_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object



@authenticate_return_auth
def add_padawan(auth_info):
  if auth_info.user.role =='admin':
    post_data = request.form if request.form else request.get_json()

    new_padawan = Padawans.new_padawan_obj()
    populate_object(new_padawan, post_data)
    try:
      db.session.add(new_padawan)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add padawan. {e}"}), 400
    
    return jsonify({"message": "padawan added", "result": padawan_schema.dump(new_padawan)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #master+ rank required, view all padawans in your temple
def get_all_padawans(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    padawan_query = db.session.query(Padawans).all()

    if not padawan_query:
      return jsonify({"message": "no padawans found"}), 404

    return jsonify({"message": "padawans retrieved", "results": padawans_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


def get_active_padawans(): #double check logic is correct
  padawan_query = db.session.query(Padawans).join(Users.is_active == True).all()

  if not padawan_query:
    return jsonify({"message": "no padawans found"}), 404

  return jsonify({"message": "padawans retrieved", "results": padawans_schema.dump(padawan_query)}), 200


@authenticate_return_auth #assigned master or Council+
def update_padawan(padawan_id,auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    post_data = request.form if request.form else request.get_json()

    if not padawan_query:
      return jsonify({"message": "unable to update record"}), 400
    
    populate_object(padawan_query, post_data)
    db.session.commit()

    return jsonify({"message": "padawan updated", "results": padawan_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #Council+ rank #promote padawan to Knight. Add extra logic
def promote_padawan(padawan_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    post_data = request.form if request.form else request.get_json()

    if not padawan_query:
      return jsonify({"message": "unable to update record"}), 400
    
    populate_object(padawan_query, post_data)
    db.session.commit()

    return jsonify({"message": "padawan updated", "results": padawan_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #Council+ rank, handle course enrollments
def delete_padawan(padawan_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
      return jsonify({"message": f"no padawan found with id {padawan_id}"}), 404
    try:
      db.session.delete(padawan_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "padawan deleted", "result": padawan_schema.dump(padawan_query)}), 200