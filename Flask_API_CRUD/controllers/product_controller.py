from flask import jsonify, request

from db import product_records


def add_product():
  post_data = request.form if request.form else request.json
  required_fields = ['product_id','product_name']
  
  for field in required_fields:
    if field not in post_data:
      return jsonify({"message": f"{field} is required to add a product"}), 400
    
  for product in product_records:
    if post_data['product_id'] == product['product_id']:
      return jsonify({"message": "Invalid input. product_id must be unique"}), 400

  if not post_data['product_id'].isnumeric():
      return jsonify({"message": "Invalid input. product_id must be a number"}), 400
  
  if post_data['product_name'].strip("/\-_., ") == "":
    return  jsonify({"message": "invalid product_name"}), 400
    
  product = {}
  product['product_id'] = post_data['product_id']
  product['product_name'] = post_data['product_name']
  product['description'] = post_data['description']
  product['price'] = post_data['price']
  if "active" in post_data:
    product['active'] = post_data['active']
  else:
    product['active'] = "true"

  product_records.append(product)

  return jsonify({"message": "product added", "result": product}), 201


def get_product_by_id(product_id):
  for product in product_records:
    if product['product_id'] == product_id:
      return jsonify({"message": "product found", "result": product}), 200
    
  return jsonify({"message": "product not found"}), 400


def get_all_products():
  return jsonify({"message": "products found", "results": product_records}), 200


def get_active_products():
  active_products = []
  for product in product_records:
    if product['active']:
      active_products.append(product)
  if active_products:
    return jsonify({"message": "products found", "results": active_products}), 200
  return jsonify({"message": "products not found"}), 400


def update_product_by_id(product_id):
  post_data = request.form if request.form else request.json

  product = {}

  for record in product_records:
    print(record['product_id'])
    if record['product_id'] == product_id:
      product = record

  if not product:
    return jsonify({"message": "product not found"}), 400

  if post_data['product_name'].strip("/\-_., ") == "":
    return  jsonify({"message": "Invalid input. product_name must contain valid characters"}), 400

  product['product_name'] = post_data.get('product_name', product['product_name'])
  product['description'] = post_data.get('description', product['description'])
  product['price'] = post_data.get('price', product['price'])
  
  if "active" in post_data:
    return jsonify({"message": "unable to update field: active"}), 400
  return jsonify({"message" : "product updated", "result": product }), 200


def update_product_activation(product_id):
  patch_data = request.form if request.form else request.json

  product = {}

  for record in product_records:
    if record['product_id'] == product_id:
      product = record

  product['active'] = patch_data.get('active', product['active'])

  return jsonify({"message" : "product updated", "result": product}), 200

  
def delete_product_by_id(product_id):
  
  for record in product_records:
    if record['product_id'] == product_id:
      product_records.remove(record)
      removed_record = record
  
  return jsonify({"message":"product deleted","result": removed_record}), 200
