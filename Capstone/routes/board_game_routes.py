from flask import Blueprint

import controllers


boardgame = Blueprint('boardgame', __name__)


@boardgame.route('/boardgame', methods=['POST'])
def add_board_game_route():
  return controllers.add_board_game()

@boardgame.route('/boardgames', methods=['GET'])
def get_board_games_route():
  return controllers.get_board_games()

@boardgame.route('/boardgames/age/<min_age>', methods=['GET'])
def get_board_games_by_age_route(min_age):
  return controllers.get_board_games_by_age(min_age)

@boardgame.route('/boardgames/players/<max_players>', methods=['GET'])
def get_board_games_by_players_route(max_players):
  return controllers.get_board_games_by_players(max_players)

@boardgame.route('/boardgame/<game_id>', methods=['GET','PUT'])
def board_game_by_id_route(game_id):
  return controllers.board_game_by_id(game_id)

@boardgame.route('/boardgame/delete', methods=['DELETE'])
def delete_board_game_route():
  return controllers.delete_board_game()
