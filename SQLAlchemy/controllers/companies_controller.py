from flask import jsonify, request

from db import db
from models.companies import Companies

def construct_record(query):
   company_record = {
    "company_id": query.company_id,
    "company_name": query.company_name
  }
   return company_record

def add_company():
  post_data = request.form if request.form else request.get_json()

  fields = ['company_name']
  required_fields = ['company_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)

    if field_data in required_fields and not field_data:
      return jsonify({"message": f"{field} is required"}), 400
    
    values[field] = field_data
    new_company = Companies(values['company_name'])

    try:
      db.session.add(new_company)
      db.session.commit()

    except:
      db.session.rollback()
      return jsonify({"message": "Could not create company"}), 400
    
    company = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()
    company_record = construct_record(company)

    return jsonify({"message": "Company created","result": company_record}), 201
  

def get_all_companies():
  companies = db.session.query(Companies).all()
  companies_list = []

  if not companies:
    return jsonify({"message": f"no company records found"}), 404

  for company in companies:
    company_record = construct_record(company)
    companies_list.append(company_record)

  return jsonify({"message": "company records found", "results": companies_list}), 200


def company_by_id(company_id):
  if company_id.isnumeric():
    return jsonify({"message": f"Invalid id. Company id must be a valid UUID"}), 400 

  company = db.session.query(Companies).filter(Companies.company_id == company_id).first()
  if not company:
    return jsonify({"message": f"company {company_id} does not exist"}), 404
  
  
  
  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()
    company.company_name = data.get("company_name", company.company_name)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update record. {e}"}), 400
    
    updated_company = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    company_record = construct_record(updated_company)
    
    return jsonify({"message": "company updated", "results": company_record}), 200
  
  elif request.method == 'GET':
    company_record = construct_record(company)

    return jsonify({"message": "product found", "results": company_record}), 200
  
  
def delete_company(company_id):
  if company_id.isnumeric():
    return jsonify({"message": f"Invalid id. Company id must be a valid UUID"}), 400 
  
  company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

  if not company:
    return jsonify({"message":f"company by id {company_id} does not exist"}), 400
  
  try:
    db.session.delete(company)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  deleted_record = construct_record(company)
  
  return jsonify({"message": "company deleted","result": deleted_record}), 200