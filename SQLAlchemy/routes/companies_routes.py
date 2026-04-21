from flask import Blueprint
import controllers

company = Blueprint('company', __name__)

@company.route ('/company', methods={'POST'})
def add_company():
  return controllers.add_company()

@company.route ('/companies', methods={'GET'})
def get_all_companies():
  return controllers.get_all_companies()

@company.route('/company/<company_id>', methods=['GET','PUT'])
def company_by_id(company_id):
  return controllers.company_by_id(company_id)

@company.route('/company/delete', methods=['DELETE'])
def delete_company():
  return controllers.delete_company()