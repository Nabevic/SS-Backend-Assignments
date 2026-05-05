from flask import jsonify, request
from db import db
from models.bgg_ratings import BGGRatings, bgg_rating_schema, bgg_ratings_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level



@authenticate_return_auth
def add_rating_(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  post_data = request.form if request.form else request.json

  new_rating = BGGRatings.new_rating_obj()
  populate_object(new_rating, post_data)

  try:
    db.session.add(new_rating)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add rating. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "rating added","result": bgg_rating_schema.dump(new_rating)}), 201

@authenticate_return_auth
def get_ratings(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  ratings_query = db.session.query(BGGRatings).all()

  if not ratings_query:
    return jsonify({"message": "no bgg ratings found"}), 404

  return jsonify({"message": "bgg ratings retrieved", "results": bgg_ratings_schema.dump(ratings_query)}), 200
  
@authenticate_return_auth
def rating_by_id(rating_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  rating_query = db.session.query(BGGRatings).filter(BGGRatings.rating_id == rating_id).first()
  if not rating_query:
    return jsonify({"message": "no bgg rating found"}), 404

  if request.method == 'GET':
    return jsonify({"message": "bgg rating retrieved", "results": bgg_rating_schema.dump(rating_query)}), 200
  
  elif request.method == "PUT":
    if auth_info.user.role not in auth_level['admin']:
      return jsonify({"message": "unauthorized"}), 401
    put_data = request.form if request.form else request.get_json()
    populate_object(rating_query, put_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update rating. {e}"}), 400
    return jsonify({"message": "bgg rating updated", "results": bgg_rating_schema.dump(rating_query)}), 200
    
  
@authenticate_return_auth
def rating_by_game_id(game_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  rating_query = db.session.query(BGGRatings).filter(BGGRatings.game_id == game_id).first()
  if not rating_query:
    return jsonify({"message": "no bgg rating found"}), 404
  return jsonify({"message": "bgg rating retrieved", "results": bgg_rating_schema.dump(rating_query)}), 200

@authenticate_return_auth
def delete_rating(auth_info):
  if auth_info.user.role not in auth_level['super']:
    return jsonify({"message": "unauthorized"}), 401
  request_data = request.form if request.form else request.json
  rating_query = db.session.query(BGGRatings).filter(BGGRatings.rating_id == request_data["rating_id"]).first()
  if not rating_query:
    return jsonify({"message": f"no rating found with id {request_data['rating_id']}"}), 400
  
  try:
    db.session.delete(rating_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "rating deleted", "result": bgg_rating_schema.dump(rating_query)}), 200