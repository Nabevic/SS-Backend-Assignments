import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class BGGRatings(db.Model):
  __tablename__ = 'BGGRatings'

  rating_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  game_id = db.Column(UUID(as_uuid=True). db.ForeignKey("BoardGames.game_id"))
  rating = db.Column(db.Float(), nullable=False)
  url = db.Column(db.String())

  board_game = db.relationship("BoardGames", foreign_keys='[BBGRatings.game_id]', back_populates='bgg_rating', uselist=False)

  def __init__(self, game_id, rating, url):
    self.game_id = game_id
    self.rating = rating
    self.url = url

  def new_rating_obj():
    return BGGRatings('',0.0,'')
  
  
class BGGRatingsSchema(ma.Schema):
  class Meta:
    fields = ['rating_id', 'game_id', 'rating', 'url']

  rating_id = ma.fields.UUID()
  game_id = ma.fields.UUID(required=True)
  rating = ma.fields.Float(required=True)
  url = ma.fields.String(allow_none=True)

bgg_rating_schema = BGGRatingsSchema()
bgg_ratings_schema = BGGRatingsSchema(many=True)