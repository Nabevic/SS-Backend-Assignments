from flask import jsonify, request
from db import db
from models.board_games import BoardGames, board_game_schema, board_games_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate



def add_board_game():
  post_data = request.form if request.form else request.json

  new_board_game = BoardGames.new_board_game_obj()
  populate_object(new_board_game, post_data)

  try:
    db.session.add(new_board_game)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add board_game. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "board_game created","result": board_game_schema.dump(new_board_game)}), 201


def get_board_games():
  board_game_query = db.session.query(BoardGames).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


def get_board_games_by_age(min_age):
  board_game_query = db.session.query(BoardGames).filter(BoardGames.min_age <= min_age).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


def get_board_games_by_players(max_players):
  board_game_query = db.session.query(BoardGames).filter(BoardGames.max_players >= max_players).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


def board_game_by_id(game_id):
  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == game_id).first()
  if not board_game_query:
    return jsonify({"message": "no board game found"}), 404

  if request.method == "PUT":
    put_data = request.form if request.form else request.get_json()
    populate_object(board_game_query, put_data)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to update board game. {e}"}), 400
    return jsonify({"message": "board game updated", "results": board_game_schema.dump(board_game_query)}), 200
    
  elif request.method == 'GET':
    return jsonify({"message": "board game retrieved", "results": board_game_schema.dump(board_game_query)}), 200
  

def delete_board_game():
  request_data = request.form if request.form else request.json
  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == request_data["game_id"]).first()
  if not board_game_query:
    return jsonify({"message": f"no board game found with id {request_data['game_id']}"}), 400
  
  try:
    db.session.delete(board_game_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "board game deleted", "result": board_game_schema.dump(board_game_query)}), 200