from flask import jsonify, request
from flask_bcrypt import generate_password_hash

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