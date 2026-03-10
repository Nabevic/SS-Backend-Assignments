from flask import jsonify, request

from db import db
from models.products import Products
from models.categories import Categories


def construct_record(query):
  categories_list = []

  for category in query.categories:
    categories_list.append({
      "category_id": category.category_id,
      "category_name": category.category_name
    })

  company_record = {
    'company_id': query.companies.company_id,
    'company_name': query.companies.company_name
  }

  if query.warranties:
    warranty_record = {
      'warranty_id': query.warranties.warranty_id,
      'warranty_months': query.warranties.warranty_months
    }
  else:
      warranty_record = {}

  product_record = {
    'product_id': query.product_id,
    'product_name': query.product_name,
    'description': query.description,
    'price': query.price,
    'active': query.active,
    'company': company_record,
    'warranty': warranty_record,
    'categories': categories_list,
  }
  return product_record
  

def add_product():
  post_data = request.form if request.form else request.get_json()

  fields = ['product_name','company_id','price','description']
  required_fields = ['product_name','company_id','price']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message":f'{field} is required'}), 400
    
    values[field] = field_data

  new_product = Products(values['company_id'],values['product_name'],values['price'], values['description'])
  try:
    db.session.add(new_product)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400

  query = db.session.query(Products).filter(Products.product_name == values['product_name']).first()
  product_record = construct_record(query)

  return jsonify({"message": "product created", "result": product_record}), 201


def add_product_category_association():
  post_data = request.form if request.form else request.get_json()

  fields = ['product_id','category_id']
  required_fields = ['product_id','category_id']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message":f"{field} is required"}), 400
    values[field] = field_data
  
  product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
  category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

  if not product_query:
    return jsonify({"message":"product id does not exist"}), 404
  
  elif not category_query:
    return jsonify({"message":"category id does not exist"}), 404

  if product_query and category_query:

    try:
      product_query.categories.append(category_query)
      db.session.commit()

    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"could not add association. {e}"}), 400

    categories_list = []
    
    for category in product_query.categories:
      categories_list.append({
        "category_id": category.category_id,
        "category_name": category.category_name
      })

    company_dict = {
      "company_id": product_query.companies.company_id,
      "category_name": product_query.companies.company_name
    }
    product = {
      'product_id': product_query.product_id,
      'product_name': product_query.product_name,
      'description': product_query.description,
      'price': product_query.price,
      'active': product_query.active,
      'company': company_dict,
      'categories': categories_list,
    }

  return jsonify({"message": "category added to product", "result": product}), 201
  



def get_all_products():
  products = db.session.query(Products).all()

  product_list = []

  for product in products:
    product_record = construct_record(product)
    product_list.append(product_record)

  return jsonify({"message": "products found", "result": product_list}), 200


def get_all_active_products():
  products = db.session.query(Products).filter(Products.active == True).all()

  product_list = []

  for product in products:
    product_record = construct_record(product)
    product_list.append(product_record)

  return jsonify({"message": "products found", "result": product_list}), 200


def product_by_id(product_id):
  if product_id.isnumeric():
    return jsonify({"message": f"Invalid id. product id must be a valid UUID"}), 400 
  
  query = db.session.query(Products).filter(Products.product_id == product_id).first()
  if not query:
    return jsonify({"message": f"product not found with id {product_id}"}), 404

  if request.method == 'PUT':
    data = request.form if request.form else request.get_json()

    query.product_name = data.get("product_name", query.product_name)
    query.company_id = data.get("company_id", query.company_id)
    query.price = data.get("price",query.price)
    query.description = data.get("description",query.description)
    query.active = data.get("active",query.active)

    try:
      db.session.commit()
    except Exception as e:
       db.session.rollback()
       return jsonify({"message:": f"unable to update record: {e}"}), 400
    
    updated_product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    product_record = construct_record(updated_product_query)

    return jsonify({"message": "product updated", "results": product_record}), 200

  elif request.method == 'GET':
    product_record = construct_record(query)

    return jsonify({"message": "product found", "result": product_record}), 200
  

def get_products_by_company_id(company_id):
  if company_id.isnumeric():
    return jsonify({"message": f"Invalid id. company id must be a valid UUID"}), 400 
  
  query = db.session.query(Products).filter(Products.company_id == company_id).all()
  if not query:
    return jsonify({"message": f"no products found with company id {company_id}"}), 404
  
  else:
    product_list = []

  for product in query:
    product_record = construct_record(product)
    product_list.append(product_record)

  return jsonify({"message": "products found", "result": product_list}), 200


def delete_product(product_id):
  if product_id.isnumeric():
    return jsonify({"message": f"Invalid id. product id must be a valid UUID"}), 400
  
  product = db.session.query(Products).filter(Products.product_id == product_id).first()
  if not product:
    return jsonify({"message": f"product not found with id {product_id}"}), 404
  
  deleted_record = construct_record(product)

  try:
    db.session.delete(product)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message":f"unable to delete product. {e}"}), 400
  
  return jsonify({"message": "product deleted","results": deleted_record})