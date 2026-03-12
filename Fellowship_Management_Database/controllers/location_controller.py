from flask import jsonify, request

from db import db
from models.location import Locations, location_schema, locations_schema
from util.reflection import populate_object


def add_location():
  post_data = request.form if request.form else request.get_json()

  new_location = Locations.new_location_obj()
  populate_object(new_location, post_data)

  try:
    db.session.add(new_location)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create location. {e}"}), 400
  
  return jsonify({"message": "location created", "results": location_schema.dump(new_location)}), 201


def location_by_id(location_id):
  location_query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

  if not location_query:
    return jsonify({"message": f"no locations found with id {location_id}"}), 404
  
  if request.method == 'PUT':
    post_data = request.form if request.form else request.get_json()
    populate_object(location_query, post_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update location. {e}"}), 400
    
    return jsonify({"message": "location updated", "results": location_schema.dump(location_query)}), 200
  
  elif request.method == 'GET':
    return jsonify({"message": "location found", "results": location_schema.dump(location_query)}), 200
  

def delete_location(location_id):
  location_query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

  if not location_query:
     return jsonify({"message": f"no locations found with id {location_id}"}), 404

  try:
    db.session.delete(location_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete location. {e}"}), 400
  
  return jsonify({"message": "location deleted", "results": location_schema.dump(location_query)}), 200