from flask import jsonify, request

from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth
from db import db


@authenticate_return_auth
def add_company(auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    try:
      db.session.add(new_company)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to create company. {e}"}), 400
    
    return jsonify({"message": "company created","result": company_schema.dump(new_company)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_all_companies(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    companies_query = db.session.query(Companies).all()

    return jsonify({"message": "companies retrieved", "result": companies_schema.dump(companies_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_company_by_id(company_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:      
        return jsonify({"message": "record not found"}), 404
    
    return jsonify({"message": "company retrieved", "results": company_schema.dump(company_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def update_company(company_id, auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
      return jsonify({"message": "company not found"}), 404
    
    populate_object(company_query, post_data)
    db.session.commit()

    return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def delete_company(auth_info):
  user_data = request.form if request.form else request.get_json()

  if auth_info.user.role == 'admin':
    company_query = db.session.query(Companies).filter(Companies.company_id == user_data["company_id"]).first()
    if not company_query:
      return jsonify({"message": f"no company found with id {user_data['company_id']}"}), 404
    try:
      db.session.delete(company_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "company deleted", "result": company_schema.dump(company_query)}), 200
  return jsonify({"message": "unauthorized"}), 401