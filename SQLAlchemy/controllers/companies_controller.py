from flask import Flask, jsonify, request

from db import db
from models.companies import Companies

def add_company():
  post_data = request.form if request.form else request.get_json()

  fields = ['company_name']
  required_fields = ['company_name']

  values = {}

  for field in fields:
    field_data = post_data.get(field)

    if field_data in required_fields and not field_data:
      return jsonify({"message": f"{field} is required"}), 400
    
    values[field] - field_data

    new_company = Companies(values['company_name'])

    try:
      db.session.add(new_company)
      db.session.commit()

    except:
      db.session.rollback()
      return jsonify({"message": "Could not create company"}), 400
    
    company = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()

    record = {
      "company_id": company.company_id,
      "company_name": company.company_name
    }

    return jsonify({"message": "Company created","result": record}), 201
  
def get_all_companies():
  companies = db.session.query(Companies).all()

  companies_list = []

  for company in companies:
    company_record = {
      "company_id": company.company_id,
      "company_name": company.company_name
    }

    companies_list.append(company_record)


def company_by_id(company_id):
  if request.method == 'GET':
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company:
      return jsonify({"message": f"company {company_id} does not exist"}), 400
      
    record = {
      'company_id' : company.company_id,
      'company_name' : company.company_name
    }

    return jsonify({"message": "product found", "results": record}), 200
  
  elif request.method == 'PUT':
    data = request.form if request.form else request.get_json()
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    company.company_name = data.get("company_name", company.company_name)

    try:
      db.session.commit()
    except:
      db.session.rollback()
      return jsonify({"message": "unable to update record"}), 400
    
    updated_company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    company = {
      'company_id': updated_company.company_id,
      'company_name': updated_company.company_name
    }
    
    return jsonify({"message": "company updated", "results": company}), 200
  
  
def delete_company(company_id):
  company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

  if not company:
    return jsonify({"message":f"company by id {company_id} does not exist"}), 400
  
  try:
    db.session.delete(company)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to delete record"}), 400
  
  return jsonify({"message": "company deleted"}), 200