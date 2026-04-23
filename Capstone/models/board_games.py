import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .board_games_categories_xref import games_categories_association_table

class BoardGames(db.Model):
  __tablename__ = 'BoardGames'

  game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  owner = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'))
  title = db.Column(db.String(), unique=True, nullable=False)
  description = db.Column(db.String())
  age_range = db.Column(db.String())
  player_count = db.Column(db.String())
  play_time = db.Column(db.Integer())

  bgg_rating = db.relationship("BGGRatings", foreign_keys='[BGGRatings.game_id]', back_populates='boardgame')
  loan = db.relationship("GameLoans", foreign_keys='[GameLoans.game_id]', back_populates='boardgame')
  categories = db.relation("Categories", secondary=games_categories_association_table, back_populates='board_games')

  def __init__(self, owner, title, description, age_range, player_count, play_time):
    self.owner = owner
    self.title = title
    self.description = description
    self.age_range = age_range
    self.player_count = player_count
    self.play_time = play_time

  def new_board_game_obj():
    return BoardGames('','','','','', 0)
  
class BoardGamesSchema(ma.Schema):
  class Meta:
    fields = ['game_id', 'owner', 'title', 'description', 'age_range', 'player_count', 'play_time', 'bbg_rating', 'loan']
    

  game_id = ma.fields.UUID()
  owner = ma.fields.UUID()
  title = ma.fields.String(required=True)
  description = ma.fields.String()
  age_range = ma.fields.String()
  player_count = ma.fields.String()
  play_time = ma.fields.Integer()

  bbg_rating = ma.fields.Nested("BGGRatingsSchema")
  loan = ma.fields.Nested("GameLoansSchema")
  # categories

board_game_schema = BoardGamesSchema()
board_games_schema = BoardGamesSchema(many=True)