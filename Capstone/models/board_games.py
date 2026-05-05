import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .board_games_categories_xref import games_categories_association_table

class BoardGames(db.Model):
  __tablename__ = 'BoardGames'

  game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  owner = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'))
  title = db.Column(db.String(), nullable=False)
  description = db.Column(db.String())
  min_age = db.Column(db.Integer())
  max_players = db.Column(db.Integer())
  play_time = db.Column(db.String())
  is_available = db.Column(db.Boolean(), default=True)

  bgg_rating = db.relationship("BGGRatings", foreign_keys='[BGGRatings.game_id]', back_populates='board_game', uselist=False)
  loan = db.relationship("GameLoans", foreign_keys='[GameLoans.game_id]', back_populates='board_game')
  categories = db.relationship("Categories", secondary=games_categories_association_table, back_populates='board_games')

  def __init__(self, owner, title, description, min_age, max_players, play_time, is_available):
    self.owner = owner
    self.title = title
    self.description = description
    self.min_age = min_age
    self.max_players = max_players
    self.play_time = play_time
    self.is_available = is_available

  def new_board_game_obj():
    return BoardGames('','','',0,0,'',True)
  
class BoardGameDetailsSchema(ma.Schema):
  class Meta:
    fields = ['game_id', 'owner', 'title', 'description', 'min_age', 'max_players', 'play_time', 'is_available', 'bgg_rating', 'categories','loan']
    
  game_id = ma.fields.UUID()
  owner = ma.fields.UUID()
  title = ma.fields.String(required=True)
  description = ma.fields.String()
  min_age = ma.fields.Integer()
  max_players = ma.fields.Integer()
  play_time = ma.fields.String()
  is_available = ma.fields.Boolean(dump_default=True)

  bgg_rating = ma.fields.Nested("BGGRatingsSchema")
  categories = ma.fields.Nested("CategoriesSchema", many=True)
  loan = ma.fields.Nested("GameLoansSchema")


class BoardGamesSchema(BoardGameDetailsSchema):
  class Meta:
    fields = ['game_id', 'owner', 'title', 'min_age', 'max_players', 'is_available', 'categories']

board_game_schema = BoardGamesSchema()
board_games_schema = BoardGamesSchema(many=True)
board_game_details_schema = BoardGameDetailsSchema()