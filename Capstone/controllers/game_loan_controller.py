from flask import jsonify, request
from db import db
from models.game_loans import GameLoans, game_loan_schema, game_loans_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level

@authenticate_return_auth
def add_loan_record(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  post_data = request.form if request.form else request.json

  new_loan = GameLoans.new_loan_obj()
  populate_object(new_loan, post_data)

  try:
    db.session.add(new_loan)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add loan. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "loan created","result": game_loan_schema.dump(new_loan)}), 201

@authenticate_return_auth
def get_loan_records(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  loan_query = db.session.query(GameLoans).all()

  if not loan_query:
    return jsonify({"message": "no records found"}), 404

  return jsonify({"message": "records retrieved", "results": game_loans_schema.dump(loan_query)}), 200

@authenticate_return_auth
def get_loan_records_by_borrower(borrower_id, auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  loan_query = db.session.query(GameLoans).filter(GameLoans.borrower_id == borrower_id).all()

  if not loan_query:
    return jsonify({"message": "no record found"}), 404

  return jsonify({"message": "records retrieved", "results": game_loans_schema.dump(loan_query)}), 200

@authenticate_return_auth
def get_loan_records_by_game(game_id, auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  loan_query = db.session.query(GameLoans).filter(GameLoans.game_id == game_id).first()

  if not loan_query:
    return jsonify({"message": "no records found"}), 404

  return jsonify({"message": "record retrieved", "results": game_loan_schema.dump(loan_query)}), 200

@authenticate_return_auth
def loan_record_by_id(loan_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  loan_query = db.session.query(GameLoans).filter(GameLoans.loan_id == loan_id).first()
  if not loan_query:
    return jsonify({"message": "no record found"}), 404

  if request.method == "PUT":
    if auth_info.user.role not in auth_level['admin']:
      return jsonify({"message": "unauthorized"}), 401
    put_data = request.form if request.form else request.get_json()
    populate_object(loan_query, put_data)

    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update loan record. {e}"}), 400
    return jsonify({"message": "loan record updated", "results": game_loan_schema.dump(loan_query)}), 200
    
  elif request.method == 'GET':
    return jsonify({"message": "loan record retrieved", "results": game_loan_schema.dump(loan_query)}), 200

@authenticate_return_auth
def delete_loan_record(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  request_data = request.form if request.form else request.json
  loan_query = db.session.query(GameLoans).filter(GameLoans.loan_id == request_data["loan_id"]).first()
  if not loan_query:
    return jsonify({"message": f"no loan found with id {request_data['loan_id']}"}), 400
  
  try:
    db.session.delete(loan_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "loan record deleted", "result": game_loan_schema.dump(loan_query)}), 200