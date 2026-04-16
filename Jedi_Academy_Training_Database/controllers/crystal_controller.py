from flask import jsonify, request

from db import db
from models.crystals import Crystals, crystal_schema, crystals_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object
from util.clearance import clearance



@authenticate_return_auth
def add_crystal(auth_info):
  if auth_info.user.force_rank in clearance['Master']:
    post_data = request.form if request.form else request.get_json()

    new_crystal = Crystals.new_crystal_obj()
    populate_object(new_crystal, post_data)
    try:
      db.session.add(new_crystal)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add crystal. {e}"}), 400
    
    return jsonify({"message": "crystal added", "result": crystal_schema.dump(new_crystal)}), 201
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Master+ rank required
def get_crystal_by_rarity(rarity_level, auth_info):
  if auth_info.user.role in clearance['Master']:
    crystal_query = db.session.query(Crystals).filter(Crystals.rarity_level == rarity_level).all()

    if not crystal_query:
      return jsonify({"message": "no crystals found"}), 404
    
    return jsonify({"message":"crystals found", "results": crystals_schema.dump(crystal_query)}), 201
  return jsonify({"message": "unauthorized"}), 401
  

