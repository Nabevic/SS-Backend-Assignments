from flask import jsonify, request

from db import db
from models.padawans import Padawans, padawan_schema, padawans_schema
from models.users import Users, user_schema, users_schema
from models.masters import Masters, master_schema, masters_schema
from lib.authenticate import authenticate_return_auth, clearance
from util.reflection import populate_object



@authenticate_return_auth
def add_padawan(auth_info):
  if auth_info.user.force_rank in clearance['Master']:
    post_data = request.form if request.form else request.get_json()

    new_padawan = Padawans.new_padawan_obj()
    populate_object(new_padawan, post_data)
    try:
      db.session.add(new_padawan)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add padawan. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "padawan added", "result": padawan_schema.dump(new_padawan)}), 201
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Master+ rank
def get_all_padawans(auth_info):
  if auth_info.user.force_rank in clearance['Master']:
    padawan_query = db.session.query(Padawans).join(Users).filter(Users.temple_id == auth_info.user.temple_id).all()

    if not padawan_query:
      return jsonify({"message": "no padawans found"}), 404

    return jsonify({"message": "padawans retrieved", "results": padawans_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



def get_active_padawans():
  padawan_query = db.session.query(Padawans).join(Users).filter(Users.is_active == True).all()

  if not padawan_query:
    return jsonify({"message": "no padawans found"}), 404

  return jsonify({"message": "padawans retrieved", "results": padawans_schema.dump(padawan_query)}), 200



@authenticate_return_auth #Assigned Master or Council+
def update_padawan(padawan_id,auth_info):
  masters_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()
  if auth_info.user.force_rank in clearance['Council'] or masters_query: 
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
  else: return jsonify({"message": "unauthorized"}), 401

  if not padawan_query:
    return jsonify({"message": "unable to update record; padawan not found"}), 404

  if auth_info.user.force_rank in clearance['Council'] or masters_query.master_id == padawan_query.master_id:
    post_data = request.form if request.form else request.get_json()
    
    populate_object(padawan_query, post_data)
    db.session.commit()

    return jsonify({"message": "padawan updated", "results": padawan_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Council+ rank
def promote_padawan(padawan_id, auth_info):
  if auth_info.user.force_rank in clearance['Council']:
    user_query = db.session.query(Users).join(Padawans).filter(Padawans.padawan_id == padawan_id and Padawans.user_id == Users.user_id).first()
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    post_data = request.form if request.form else request.get_json()

    if not padawan_query or not user_query:
      return jsonify({"message": "unable to update record"}), 400
    
    populate_object(user_query, post_data)
    try:
      db.session.delete(padawan_query)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "padawan promoted", "results": user_schema.dump(user_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Council+
def delete_padawan(padawan_id, auth_info):
  if auth_info.user.force_rank in clearance['Council']:
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
      return jsonify({"message": f"no padawan found with id {padawan_id}"}), 404
    try:
      db.session.delete(padawan_query)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "padawan deleted", "result": padawan_schema.dump(padawan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401