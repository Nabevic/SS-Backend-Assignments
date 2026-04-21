from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema, user_profile_schema
from models.temples import Temples, temples_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, clearance



def add_user():
  post_data = request.form if request.form else request.json
  temple_query = db.session.query(Temples).filter(Temples.temple_id == post_data['temple_id']).first()
  if not temple_query:
    return jsonify({"message": f"invalid temple id; no temple found with id {post_data['temple_id']}"}), 404

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



@authenticate_return_auth #Council+ rank
def get_all_users(auth_info):
  if auth_info.user.force_rank in clearance['Council']:
    user_query = db.session.query(Users).all()

    if not user_query:
      return jsonify({"message": "no users found"}), 404

    return jsonify({"message": "users retrieved", "results": users_schema.dump(user_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate
def user_by_id(user_id):
  user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

  if not user_query:
    return jsonify({"message": "no user found"}), 404

  return jsonify({"message": "user retrieved", "results": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def get_user_profile(auth_info):
  user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

  if not user_query:
    return jsonify({"message": "no user found"}), 404

  return jsonify({"message": "user retrieved", "results": user_profile_schema.dump(user_query)}), 200



@authenticate_return_auth #Grand Master rank
def delete_user(user_id, auth_info):
  if auth_info.user.force_rank in clearance['GrandMaster']:
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
  return jsonify({"message": "unauthorized"}), 401