from flask import jsonify, request
from db import db
from models.game_loans import GameLoans, game_loan_schema, game_loans_schema
from models.board_games import BoardGames, board_game_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level
from datetime import datetime



def update_game_availability(board_game_id, status=False):
  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == board_game_id).first()
  if not board_game_query:
    return
  update_available = {"is_available": status} 
  try:
    populate_object(board_game_query, update_available)
    db.session.commit()
  except Exception:
    db.session.rollback()
  return 



@authenticate_return_auth
def add_loan_record(auth_info):
  post_data = request.form if request.form else request.json

  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == post_data['game_id']).first()
  if not board_game_query:
    return jsonify({"message": f"unable to checkout boardgame. boardgame with id {post_data['game_id']} does not exist"}), 404

  if auth_info.user.user_id == board_game_query.owner or auth_info.user.role in auth_level['admin']:
    
    if not board_game_query.is_available:
      return jsonify({"message": f"unable to checkout boardgame. boardgame already checked out"}), 400

    new_loan = GameLoans.new_loan_obj()
    populate_object(new_loan, post_data)

    try:
      db.session.add(new_loan)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to checkout boardgame. {e}"}), 400
    
    update_available = {"is_available": False} 
    populate_object(board_game_query, update_available)

    db.session.commit()
    return jsonify({"message": "boardgame checked out","result": game_loan_schema.dump(new_loan)}), 201
  
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth
def get_loan_records(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401
  loan_query = db.session.query(GameLoans).all()

  if not loan_query:
    return jsonify({"message": "no records found"}), 404

  return jsonify({"message": "records retrieved", "results": game_loans_schema.dump(loan_query)}), 200



@authenticate_return_auth
def get_loan_records_by_borrower(borrower_id, auth_info):
  if auth_info.user.user_id == borrower_id or auth_info.user.role in auth_level['admin']:
    loan_query = db.session.query(GameLoans).filter(GameLoans.borrower_id == borrower_id).all()

    if not loan_query:
      return jsonify({"message": "no record found"}), 404

    return jsonify({"message": "records retrieved", "results": game_loans_schema.dump(loan_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth
def get_loan_records_by_game(game_id, auth_info):
  loan_query = db.session.query(GameLoans).join(BoardGames).filter(GameLoans.game_id == game_id).first()
  if not loan_query:
    return jsonify({"message": "no records found"}), 404
  
  if auth_info.user.user_id != loan_query.board_game.owner or auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401

  return jsonify({"message": "record retrieved", "results": game_loan_schema.dump(loan_query)}), 200



@authenticate_return_auth
def loan_record_by_id(loan_id, auth_info):
  loan_query = db.session.query(GameLoans).join(BoardGames).filter(GameLoans.loan_id == loan_id).first()
  if not loan_query:
    return jsonify({"message": "no record found"}), 404
  
  if request.method == 'GET':
    if auth_info.user.user_id == loan_query.board_game.owner or auth_info.user.user_id == loan_query.borrower_id or auth_info.user.role in auth_level['admin']:
      return jsonify({"message": "loan record retrieved", "results": game_loan_schema.dump(loan_query)}), 200
    return jsonify({"message": "unauthorized"}), 401
  
  elif request.method == "PUT":
    if auth_info.user.user_id == loan_query.board_game.owner or auth_info.user.role in auth_level['admin']:
      put_data = request.form if request.form else request.get_json()
      if "date_returned" in put_data:
        update_game_availability(loan_query.game_id, True)
        
      populate_object(loan_query, put_data)
      
      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"unable to update loan record. {e}"}), 400
      return jsonify({"message": "loan record updated", "results": game_loan_schema.dump(loan_query)}), 200
    return jsonify({"message": "unauthorized"}), 401
  


@authenticate_return_auth
def loan_record_return(loan_id, auth_info):
  loan_query = db.session.query(GameLoans).join(BoardGames).filter(GameLoans.loan_id == loan_id).first()
  if not loan_query:
    return jsonify({"message": "no record found"}), 404
  
  if auth_info.user.user_id == loan_query.board_game.owner or auth_info.user.role in auth_level['admin']:

    date_returned = {"date_returned": datetime.today()}

    update_game_availability(loan_query.game_id, True)
    populate_object(loan_query, date_returned)
    
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update loan record. {e}"}), 400
    return jsonify({"message": "loan record updated", "results": game_loan_schema.dump(loan_query)}), 200
  
  return jsonify({"message": "unauthorized"}), 401
    


@authenticate_return_auth
def delete_loan_record(auth_info):
  if auth_info.user.role not in auth_level['super']:
    return jsonify({"message": "unauthorized"}), 401
  
  request_data = request.form if request.form else request.json
  loan_query = db.session.query(GameLoans).filter(GameLoans.loan_id == request_data["loan_id"]).first()
  if not loan_query:
    return jsonify({"message": f"no loan found with id {request_data['loan_id']}"}), 404
  
  try:
    db.session.delete(loan_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "loan record deleted", "result": game_loan_schema.dump(loan_query)}), 200