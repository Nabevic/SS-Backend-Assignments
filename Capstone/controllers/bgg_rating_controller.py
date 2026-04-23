from flask import jsonify, request
from db import db
from models.bgg_ratings import BGGRatings, bgg_rating_schema, bgg_ratings_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate



def add_rating_():
  pass
def get_ratings():
  pass
def rating_by_id(rating_id):
  pass
def rating_by_game_id(game_id):
  pass
def delete_rating():
  pass