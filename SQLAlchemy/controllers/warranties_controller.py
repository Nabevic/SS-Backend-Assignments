from flask import Flask, jsonify, request

from db import db
from models.warranties import Warranties
from models.products import Products

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

  new_warranty = Warranties(values['product_id','warranty_months'])

  try:
    db.session.add(new_warranty)
    db.session.commit()
  except:
    db.session.rollback()
    return jsonify({"message": "unable to create record"}), 400
  
  query = db.session.query(Warranties).filter(Warranties.product_id == values['product_id']).first()

  values['warranty_id'] = query.warranty_id

  return jsonify({"message": "category created", "result": values}), 201