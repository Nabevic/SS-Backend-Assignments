from flask import Blueprint

import controllers


boardgame = Blueprint('boardgame', __name__)


@boardgame.route('/boardgame', methods=['POST'])
def add_boardgame_route():
  return controllers.add_boardgame()

@boardgame.route('/boardgames', methods=['GET'])
def get_boardgames_route():
  return controllers.get_boardgames()

@boardgame.route('/boardgames/<age_range>', methods=['GET'])
def get_boardgames_by_age_route(age_range):
  return controllers.get_boardgames_by_age(age_range)

@boardgame.route('/boardgames/<player_count>', methods=['GET'])
def get_boardgames_by_players_route(player_count):
  return controllers.get_boardgames_by_players(player_count)

@boardgame.route('/boardgame/<boardgame_id>', methods=['GET','PUT'])
def boardgame_by_id_route(boardgame_id):
  return controllers.boardgame_by_id(boardgame_id)

@boardgame.route('/boardgame/delete', methods=['DELETE'])
def delete_boardgame_route():
  return controllers.delete_boardgame()