from flask import jsonify, request
from db import db
from models.categories import Categories, category_schema, categories_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate



@authenticate_return_auth
def add_category(auth_info):
  if auth_info.user.role == 'admin':
    post_data = request.form if request.form else request.get_json()

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
      db.session.add(new_category)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to create category. {e}"}), 400

    return jsonify({"message": "category created","result": category_schema.dump(new_category)}), 201
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def get_all_categories(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    categories_query = db.session.query(Categories).all()

    return jsonify({"message": "categories retrieved", "result": categories_schema.dump(categories_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def category_by_id(category_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
        category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
  if not category_query:
    return jsonify({"message": "no category found"}), 404

  if request.method == "PUT":
    put_data = request.form if request.form else request.get_json()
    populate_object(category_query, put_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update category. {e}"}), 400
    return jsonify({"message": "category updated", "results": category_schema.dump(category_query)}), 200
    
  elif request.method == 'GET':
    return jsonify({"message": "category retrieved", "results": category_schema.dump(category_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def delete_category(auth_info):
  user_data = request.form if request.form else request.get_json()

  if auth_info.user.role == 'admin':
    category_query = db.session.query(Categories).filter(Categories.category_id == user_data["category_id"]).first()
    if not category_query:
      return jsonify({"message": f"no category found with id {user_data['category_id']}"}), 404
    try:
      db.session.delete(category_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "category deleted", "result": category_schema.dump(category_query)}), 200
  return jsonify({"message": "unauthorized"}), 401