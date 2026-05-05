from flask import jsonify, request
from db import db
from models.board_games import BoardGames, board_game_schema, board_games_schema, board_game_details_schema
from models.categories import Categories
from models.board_games_categories_xref import games_categories_association_table
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level



@authenticate_return_auth
def add_board_game(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  post_data = request.form if request.form else request.json

  new_board_game = BoardGames.new_board_game_obj()
  populate_object(new_board_game, post_data)

  try:
    db.session.add(new_board_game)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add boardgame. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "boardgame created","result": board_game_details_schema.dump(new_board_game)}), 201


@authenticate_return_auth
def add_board_game_category(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401 
  
  post_data = request.form if request.form else request.json

  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == post_data['game_id']).first()
  category_query = db.session.query(Categories).filter(Categories.category_id == post_data['category_id']).first()

  if not board_game_query:
    return jsonify({"message":"boardgame id does not exist"}), 404
  
  elif not category_query:
    return jsonify({"message":"category id does not exist"}), 404

  if board_game_query and category_query:
    board_game_query.categories.append(category_query)
    db.session.commit()

  return jsonify({"message": "category added to boardgame", "result": board_game_details_schema.dump(board_game_query)}), 201


@authenticate_return_auth
def get_board_games(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  board_game_query = db.session.query(BoardGames).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


@authenticate_return_auth
def get_board_games_by_owner(user_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  board_game_query = db.session.query(BoardGames).filter(BoardGames.owner == user_id).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


@authenticate_return_auth
def get_board_games_by_players(max_players, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  board_game_query = db.session.query(BoardGames).filter(BoardGames.max_players >= max_players).all()

  if not board_game_query:
    return jsonify({"message": "no board games found"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


@authenticate_return_auth
def get_board_games_by_category(category_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  board_game_query = db.session.query(BoardGames).join(games_categories_association_table).join(Categories).filter(Categories.category_id == category_id).all()

  if not board_game_query:
    return jsonify({"message": f"no board games found with category id {category_id}"}), 404

  return jsonify({"message": "board games retrieved", "results": board_games_schema.dump(board_game_query)}), 200


@authenticate_return_auth
def board_game_by_id(game_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == game_id).first()
  if not board_game_query:
    return jsonify({"message": "no board game found"}), 404
  

  if request.method == 'GET':
    return jsonify({"message": "board game retrieved", "results": board_game_details_schema.dump(board_game_query)}), 200

  elif request.method == "PUT":
    if auth_info.user.user_id == board_game_query.owner or auth_info.user.role in auth_level['admin']:
      put_data = request.form if request.form else request.get_json()
      populate_object(board_game_query, put_data)
      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"unable to update board game. {e}"}), 400
      return jsonify({"message": "board game updated", "results": board_game_details_schema.dump(board_game_query)}), 200
    return jsonify({"message": "unauthorized"}), 401
    
  

@authenticate_return_auth
def remove_board_game_category(auth_info):
  if auth_info.user.role not in auth_level['admin']:
    return jsonify({"message": "unauthorized"}), 401 
  
  post_data = request.form if request.form else request.json

  board_game_query = db.session.query(BoardGames).filter(BoardGames.game_id == post_data['game_id']).first()
  category_query = db.session.query(Categories).filter(Categories.category_id == post_data['category_id']).first()
  assoc_query = db.session.query(BoardGames).filter(BoardGames.game_id == post_data['game_id'] and BoardGames.categories.category_id == post_data['category_id']).first()
  if not board_game_query:
    return jsonify({"message":"unable to remove category from boardgame, boardgame id is invalid"}), 404
  
  elif not category_query:
    return jsonify({"message":"unable to remove category from boardgame, category id is invalid"}), 404

  if not assoc_query:
    return jsonify({"message":"unable to remove category from boardgame, category isn't associated with selected boardgame"}), 400

  try:
    board_game_query.categories.remove(category_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to remove association. {e}"}), 400
    
  db.session.commit()
  return jsonify({"message": "category association removed", "result": board_game_schema.dump(board_game_query)}), 200


@authenticate_return_auth
def delete_board_game(auth_info):
  if auth_info.user.role not in auth_level['super']:
    return jsonify({"message": "unauthorized"}), 401
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
  return jsonify({"message": "board game deleted", "result": board_game_details_schema.dump(board_game_query)}), 200