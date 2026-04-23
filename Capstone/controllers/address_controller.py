from flask import jsonify, request
from db import db
from models.addresses import Addresses, address_schema, addresses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate





def add_address():
  post_data = request.form if request.form else request.json

  new_address = Addresses.new_address_obj()
  populate_object(new_address, post_data)


  try:
    db.session.add(new_address)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add address. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "address created","result": address_schema.dump(new_address)}), 201


@authenticate_return_auth 
def get_all_addresses(auth_info):
  address_query = db.session.query(Addresses).all()

  if not address_query:
    return jsonify({"message": "no addresses found"}), 404

  return jsonify({"message": "addresses retrieved", "results": addresses_schema.dump(address_query)}), 200


@authenticate_return_auth 
def address_by_id(address_id, auth_info):
  address_query = db.session.query(Addresses).filter(Addresses.address_id == address_id).first()
  if not address_query:
    return jsonify({"message": "no address found"}), 404

  if request.method == "PUT":
    put_data = request.form if request.form else request.get_json()
    populate_object(address_query, put_data)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update address. {e}"}), 400
    return jsonify({"message": "address updated", "results": address_schema.dump(address_query)}), 200
    
  elif request.method == 'GET':
    return jsonify({"message": "address retrieved", "results": address_schema.dump(address_query)}), 200



@authenticate_return_auth
def delete_address(auth_info):
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
