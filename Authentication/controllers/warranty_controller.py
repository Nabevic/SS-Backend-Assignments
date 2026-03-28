from flask import jsonify, request

from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth
from db import db


@authenticate_return_auth
def add_warranty(auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()

    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)

    try:
      db.session.add(new_warranty)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to create warranty. {e}"}), 400

    return jsonify({"message": "warranty created","result": warranty_schema.dump(new_warranty)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_warranty_by_id(warranty_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:      
        return jsonify({"message": "record not found"}), 404
    
    return jsonify({"message": "warranty retrieved", "results": warranty_schema.dump(warranty_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def update_warranty(warranty_id, auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
      return jsonify({"message": "warranty not found"}), 404
    
    populate_object(warranty_query, post_data)
    db.session.commit()

    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def delete_warranty(auth_info):
  user_data = request.form if request.form else request.get_json()

  if auth_info.user.role == 'admin':
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == user_data["warranty_id"]).first()
    if not warranty_query:
      return jsonify({"message": f"no warranty found with id {user_data['warranty_id']}"}), 404
    try:
      db.session.delete(warranty_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "warranty deleted", "result": warranty_schema.dump(warranty_query)}), 200
  return jsonify({"message": "unauthorized"}), 401