from flask import jsonify, request

from db import db
from models.species import Species, species_schema, many_species_schema
from lib.authenticate import authenticate_return_auth, clearance
from util.reflection import populate_object



@authenticate_return_auth
def add_species(auth_info):
  if auth_info.user.force_rank in clearance['Master']:
    post_data = request.form if request.form else request.get_json()

    new_species = Species.new_species_obj()
    populate_object(new_species, post_data)
    try:
      db.session.add(new_species)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add species. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "species added", "result": species_schema.dump(new_species)}), 201
  return jsonify({"message": "unauthorized"}), 401



def get_species(species_id):
  species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

  if not species_query:
    return jsonify({"message": "no species found"}), 404

  return jsonify({"message": "species retrieved", "results": species_schema.dump(species_query)}), 200