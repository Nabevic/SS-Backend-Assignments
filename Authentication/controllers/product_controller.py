from flask import jsonify, request

from db import db
from models.product import Products, product_schema, products_schema
from models.category import Categories, category_schema, categories_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object


@authenticate_return_auth
def add_product(auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    try:
      db.session.add(new_product)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to create product. {e}"}), 400
    
    return jsonify({"message": "product created","result": product_schema.dump(new_product)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def add_product_category_association(product_id, category_id, auth_info):
  if auth_info.user.role == 'admin':
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not product_query:
      return jsonify({"message":"product id does not exist"}), 404
    
    elif not category_query:
      return jsonify({"message":"category id does not exist"}), 404

    if product_query and category_query:
      product_query.categories.append(category_query)
      db.session.commit()

    return jsonify({"message": "category added to product", "result": product_schema.dump(product_query)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_all_products(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    products_query = db.session.query(Products).all()

    if not products_query:
      return jsonify({"message": "no products found"}), 404

    return jsonify({"message": "products retrieved", "results": products_schema.dump(products_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_active_products(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    products_query = db.session.query(Products).filter(Products.active == True).all()

    return jsonify({"message": "products retrieved", "results": products_schema.dump(products_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_product_by_id(product_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:      
        return jsonify({"message": "record not found"}), 404
    
    return jsonify({"message": "product retrieved", "results": product_schema.dump(product_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_products_by_company_id(company_id, auth_info): 
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not products_query:
      return jsonify({"message": f"no products found with company id {company_id}"}), 404

    return jsonify({"message": "products retrieved", "results": products_schema.dump(products_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def update_product_by_id(product_id, auth_info):
  if auth_info.user.role == 'admin':
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    post_data = request.form if request.form else request.get_json()

    if not product_query:
        return jsonify({"message": "unable to update record"}), 400
    
    populate_object(product_query, post_data)

    db.session.commit()

    return jsonify({"message": "product updated", "results": product_schema.dump(product_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def delete_product(auth_info):
  user_data = request.form if request.form else request.get_json()

  if auth_info.user.role == 'admin':
    product_query = db.session.query(Products).filter(Products.product_id == user_data["product_id"]).first()
    if not product_query:
      return jsonify({"message": f"no product found with id {user_data['product_id']}"}), 404
    try:
      db.session.delete(product_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "product deleted", "result": product_schema.dump(product_query)}), 200
  return jsonify({"message": "unauthorized"}), 401