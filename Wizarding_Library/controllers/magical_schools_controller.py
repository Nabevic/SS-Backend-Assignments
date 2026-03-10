from flask import Flask, jsonify, request

from db import db
from models.magical_schools import MagicalSchools

def construct_record(query):
  school_record = {
    "school_id": query.school_id,
    "school_name": query.school_name,
    "location": query.location,
    "founded_year": query.founded_year,
    "headmaster": query.headmaster
  }
  return school_record


def add_school():
  post_data = request.form if request.form else request.get_json()

  fields = ["school_name", "location", "founded_year", "headmaster"]
  required_fields = ['school_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message": f'{field} is required'}), 400
    values[field] = field_data
  
  new_school = MagicalSchools(values["school_name"], values["location"], values["founded_year"], values["headmaster"])

  try:
    db.session.add(new_school)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400 
  
  query = db.session.query(MagicalSchools).filter(MagicalSchools.school_name == values['school_name']).first()
  school_record = construct_record(query)

  return jsonify({"message": "school created", "result": school_record}), 201
  

def get_schools():
  schools_query = db.session.query(MagicalSchools).all()

  if not schools_query:
    return jsonify({"message": "no school found"}), 404

  school_list = []
  for school in schools_query:
    school_record = construct_record(school)
    school_list.append(school_record)

  return jsonify({"message": "schools found", "result": school_list})
  
def school_by_id(school_id):
  school_query = db.session.query(MagicalSchools).filter(MagicalSchools.school_id == school_id).first()

  if not school_query:
    return jsonify({"message": f"school not found with id {school_id}"}), 404
  
  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()

    school_query.school_name = data.get("school_name", school_query.school_name)
    school_query.location = data.get("location", school_query.location)
    school_query.founded_year = data.get("founded_year", school_query.founded_year)
    school_query.headmaster = data.get("headmaster",school_query.headmaster)

    try:
      db.session.commit()
    except Exception as e:
       db.session.rollback()
       return jsonify({"message:": f"unable to update record: {e}"}), 400
    
    updated_school_query = db.session.query(MagicalSchools).filter(MagicalSchools.school_id == school_id).first()
    school_record = construct_record(updated_school_query)

    return jsonify({"message": "school updated", "results": school_record}), 200

  elif request.method == 'GET':
    school_record = construct_record(school_query)

    return jsonify({"message": "school found", "result": school_record}), 200


def delete_school(school_id):
  school_query = db.session.query(MagicalSchools).filter(MagicalSchools.school_id == school_id).first()

  if not school_query:
    return jsonify({"message": f"school not found with id {school_id}"}), 404

  deleted_record = construct_record(school_query)

  try:
    db.session.delete(school_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message":f"unable to delete school. {e}"}), 400
  
  return jsonify({"message": "school deleted","results": deleted_record})