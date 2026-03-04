from flask import jsonify, request

from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object
from db import db


def add_warranty():
  post_data = request.form if request.form else request.json

  new_warranty = Warranties.new_warranty_obj()
  populate_object(new_warranty, post_data)

  db.session.add(new_warranty)

  return jsonify({"message": "warranty created","result": warranty_schema.dump(new_warranty)}), 201

def get_all_warranties():
  warranties_query = db.session.query(Warranties).all()

  return jsonify({"message": "warranties retrieved", "result": warranties_schema.dump(warranties_query)}), 200

def update_warranty_by_id(warranty_id):
  post_data = request.form if request.form else request.json
  warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

  if not warranty_query:
    return jsonify({"message": "warranty not found"}), 404
  
  populate_object(warranty_query, post_data)
  db.session.commit()

  return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200
