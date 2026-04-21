from flask import jsonify, request

from db import db
from models.warranties import Warranties



def construct_record(query):
   warranty_record = {
    "warranty_id": query.warranty_id,
    "product_id": query.product_id,
    "warranty_months": query.warranty_months
  }
   return warranty_record


def add_warranty():
  post_data = request.form if request.form else request.get_json()

  fields = ['product_id', 'warranty_months']
  required_fields = ['product_id','warranty_months']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message":f'{field} is required'}), 400
    
    values[field] = field_data

  new_warranty = Warranties(values['product_id'],values['warranty_months'])

  try:
    db.session.add(new_warranty)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400
  
  query = db.session.query(Warranties).filter(Warranties.product_id == values['product_id']).first()

  values['warranty_id'] = query.warranty_id

  return jsonify({"message": "category created", "result": values}), 201

def warranty_by_id(warranty_id):
  warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
  if not warranty:
    return jsonify({"message": f"warranty {warranty_id} does not exist"}), 400
  

  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()
    warranty.warranty_months = data.get("warranty_months", warranty.warranty_months)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update record. {e}"}), 400
    
    updated_warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    warranty_record = construct_record(updated_warranty)
    
    return jsonify({"message": "warranty updated", "results": warranty_record}), 200
  

  elif request.method == 'GET':
    warranty_record = construct_record(warranty)

    return jsonify({"message": "warranty found", "results": warranty_record}), 200
  
  
def delete_warranty():
  post_data = request.form if request.form else request.get_json()
  warranty = db.session.query(Warranties).filter(Warranties.warranty_id == post_data["warranty_id"]).first()

  if not warranty:
    return jsonify({"message":f"warranty by id {post_data["warranty_id"]} does not exist"}), 400
  
  else: 
    deleted_record = construct_record(warranty)

  try:
    db.session.delete(warranty)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  return jsonify({"message": "warranty deleted", "result": deleted_record}), 200
