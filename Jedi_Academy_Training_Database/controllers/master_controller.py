from flask import jsonify, request

from db import db
from models.masters import Masters, master_schema, masters_schema
from models.padawans import Padawans
from lib.authenticate import authenticate_return_auth, clearance
from util.reflection import populate_object



@authenticate_return_auth
def add_master(auth_info):
  if auth_info.user.force_rank in clearance['Council']:
    post_data = request.form if request.form else request.get_json()

    new_master = Masters.new_master_obj()
    populate_object(new_master, post_data)
    try:
      db.session.add(new_master)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add master. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "master added", "result": master_schema.dump(new_master)}), 201
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Padawan+
def get_all_masters(auth_info):
  if auth_info.user.force_rank in clearance['Padawan']:
    master_query = db.session.query(Masters).all()

    if not master_query:
      return jsonify({"message": "no masters found"}), 404

    return jsonify({"message": "masters retrieved", "results": masters_schema.dump(master_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Self or Council+
def update_master(master_id, auth_info):
  master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()
  if not master_query:
    return jsonify({"message": "unable to update record; master not found"}), 400
  
  if auth_info.user.force_rank in clearance['Council'] or auth_info.user.user_id == master_query.user_id:
    post_data = request.form if request.form else request.get_json()

      
    populate_object(master_query, post_data)
    db.session.commit()

    return jsonify({"message": "master updated", "results": master_schema.dump(master_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Grand Master
def delete_master(master_id, auth_info):
  if auth_info.user.force_rank not in clearance['GrandMaster']:
    return jsonify({"message": "unauthorized"}), 401
  
  master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()
  padawan_query = db.session.query(Padawans).filter(Padawans.master_id == master_id).first()

  if padawan_query:
    return jsonify({"message": f"padawan found associated with master. reassign padawan {padawan_query.padawan_id}: {padawan_query.padawan_name} to a new master to continue."}), 404

  if not master_query:
    return jsonify({"message": f"no master found with id {master_id}"}), 404
  try:
    db.session.delete(master_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "master deleted", "result": master_schema.dump(master_query)}), 200