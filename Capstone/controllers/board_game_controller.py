from flask import jsonify, request
from db import db
from models.board_games import BoardGames, board_game_schema, board_games_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate



def add_boardgame():
  pass
def get_boardgames():
  pass
def get_boardgames_by_age(age_range):
  pass
def get_boardgames_by_players(player_count):
  pass
def boardgame_by_id(boardgame_id):
  pass
def delete_boardgame():
  pass