from flask import jsonify, request
from db import db
from models.addresses import Addresses, address_schema, addresses_schema
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level




@authenticate_return_auth
def add_address(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  
  post_data = request.form if request.form else request.json

  new_address = Addresses.new_address_obj()
  populate_object(new_address, post_data)

  try:
    db.session.add(new_address)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add address. {e}"}), 400

  db.session.commit()

  if auth_info.user.role == 'user' and auth_info.user.user_address == 'null':
    user_query = db.session.query(Users).filter(Users.user_id == auth_info.user.user_id).first()
    user_address = address_schema.dump(new_address)
    populate_object(user_query, {"user_address": user_address["address_id"]})
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add address to user. {e}"}), 400

  return jsonify({"message": "address created","result": address_schema.dump(new_address)}), 201


@authenticate_return_auth 
def get_all_addresses(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  
  address_query = db.session.query(Addresses).all()

  if not address_query:
    return jsonify({"message": "no addresses found"}), 404

  return jsonify({"message": "addresses retrieved", "results": addresses_schema.dump(address_query)}), 200


@authenticate_return_auth 
def address_by_id(address_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  
  address_query = db.session.query(Addresses).filter(Addresses.address_id == address_id).first()
  if not address_query:
    return jsonify({"message": "no address found"}), 404

  if request.method == 'GET':
    return jsonify({"message": "address retrieved", "results": address_schema.dump(address_query)}), 200
  
  elif request.method == "PUT":
    if str(auth_info.user.user_address) == str(address_id) or auth_info.user.role in auth_level['super']:
    
      put_data = request.form if request.form else request.get_json()
      populate_object(address_query, put_data)
      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"unable to update address. {e}"}), 400
      return jsonify({"message": "address updated", "results": address_schema.dump(address_query)}), 200
    return jsonify({"message": "unauthorized"}), 401
    



@authenticate_return_auth
def delete_address(auth_info):
  if auth_info.user.role not in auth_level['super']:
    return jsonify({"message": "unauthorized"}), 401
  request_data = request.form if request.form else request.json
  address_query = db.session.query(Addresses).filter(Addresses.address_id == request_data["address_id"]).first()
  if not address_query:
    return jsonify({"message": f"no address found with id {request_data['address_id']}"}), 400
  
  try:
    db.session.delete(address_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "address deleted", "result": address_schema.dump(address_query)}), 200
