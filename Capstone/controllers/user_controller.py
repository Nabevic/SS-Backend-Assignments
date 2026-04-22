from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate



def add_user():
  post_data = request.form if request.form else request.json

  new_user = Users.new_user_obj()
  populate_object(new_user, post_data)

  new_user.password = generate_password_hash(new_user.password).decode('utf8')

  try:
    db.session.add(new_user)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add user. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "user created","result": user_schema.dump(new_user)}), 201



@authenticate_return_auth 
def get_all_users(auth_info):
  user_query = db.session.query(Users).all()

  if not user_query:
    return jsonify({"message": "no users found"}), 404

  return jsonify({"message": "users retrieved", "results": users_schema.dump(user_query)}), 200



@authenticate_return_auth 
def user_by_id(user_id, auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": "no user found"}), 404

  return jsonify({"message": "user retrieved", "results": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def get_user_profile(auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

  if not user_query:
    return jsonify({"message": "no user found"}), 404

  return jsonify({"message": "user retrieved", "results": user_schema.dump(user_query)}), 200



@authenticate_return_auth
def delete_user(user_id, auth_info):

  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": f"no user found with id {user_id}"}), 404
  try:
    db.session.delete(user_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "user deleted", "result": user_schema.dump(user_query)}), 200
