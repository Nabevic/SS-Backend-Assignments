from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.user import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate




def add_user():
  post_data = request.form if request.form else request.json

  new_user = Users.new_user_obj()

  populate_object(new_user, post_data)

  new_user.password = generate_password_hash(new_user.password).decode('utf8')

  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "user created","result": user_schema.dump(new_user)}), 201


@authenticate
def get_all_users():
  users_query = db.session.query(Users).all()

  return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200


@authenticate_return_auth
def user_by_id(user_id, auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()


  if auth_info.user.role == 'admin' or user_id == str(auth_info.user.user_id):
    if not user_query:
      return jsonify({"message": f"no user found with id {user_id}"}), 404
    
    if request.method == 'PUT':
      put_data = request.form if request.form else request.get_json()
      populate_object(user_query, put_data)

      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"unable to update user. {e}"}), 400
      return jsonify({"message": "hero updated", "results": user_schema.dump(user_query)}), 200
    
    elif request.method == 'GET':
      return jsonify({"message": "user found", "result":user_schema.dump(user_query)}), 200
  
  return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth
def delete_user(auth_info):
  user_data = request.form if request.form else request.get_json()

  if auth_info.user.role == 'admin':
    user_query = db.session.query(Users).filter(Users.user_id == user_data["user_id"]).first()
    if not user_query:
      return jsonify({"message": f"no user found with id {user_data['user_id']}"}), 404
    try:
      db.session.delete(user_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "warranty deleted", "result": user_schema.dump(user_query)}), 200
  return jsonify({"message": "unauthorized"}), 401