from flask import jsonify, request

from db import db
from models.temples import Temples, temple_schema, temples_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object



# @authenticate_return_auth
def add_temple():
  # if auth_info.user.role =='admin':
    post_data = request.form if request.form else request.get_json()

    new_temple = Temples.new_temple_obj()
    populate_object(new_temple, post_data)
    try:
      db.session.add(new_temple)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add temple. {e}"}), 400
    
    return jsonify({"message": "temple added", "result": temple_schema.dump(new_temple)}), 201
  # return jsonify({"message": "unauthorized"}), 401



def get_temple(temple_id):
  temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

  if not temple_query:
    return jsonify({"message": "no temple found"}), 404

  return jsonify({"message": "temple retrieved", "results": temple_schema.dump(temple_query)}), 200

@authenticate_return_auth #Grand Master rank
def update_temple(temple_id, auth_info): 
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    post_data = request.form if request.form else request.get_json()

    if not temple_query:
      return jsonify({"message": "unable to update record"}), 400
    
    populate_object(temple_query, post_data)
    db.session.commit()

    return jsonify({"message": "temple updated", "results": temple_schema.dump(temple_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #Grand Master rank, relocate members
def delete_temple(temple_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if not temple_query:
      return jsonify({"message": f"no temple found with id {temple_id}"}), 404
    try:
      db.session.delete(temple_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "temple deleted", "result": temple_schema.dump(temple_query)}), 200
  return jsonify({"message": "unauthorized"}), 401

