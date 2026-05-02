from flask import Blueprint

import controllers


rating = Blueprint('rating', __name__)


@rating.route('/rating', methods=['POST'])
def add_rating_route():
  return controllers.add_rating_()

@rating.route('/ratings', methods=['GET'])
def get_ratings_route():
  return controllers.get_ratings()

@rating.route('/rating/<rating_id>', methods=['GET', 'PUT'])
def rating_by_id_route(rating_id):
  return controllers.rating_by_id(rating_id)

@rating.route('/rating/game/<game_id>', methods=['GET'])
def rating_by_game_id_route(game_id):
  return controllers.rating_by_game_id(game_id)

@rating.route('/rating/delete', methods=['DELETE'])
def delete_rating_route():
  return controllers.delete_rating()