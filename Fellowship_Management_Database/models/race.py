import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Races(db.Model):
  __tablename__ = "Races"

  race_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  race_name = db.Column(db.String(), unique=True, nullable=False)
  homeland = db.Column(db.String())
  lifespan = db.Column(db.Integer())

  heroes = db.relationship("Heroes", foreign_keys='[Races.race_id]', back_populates='Races', cascade='all')

  def __init__(self, race_name, homeland, lifespan):
    self.race_name = race_name
    self.homeland = homeland
    self.lifespan = lifespan

  def new_hero_obj():
    return Races('', '', 0) 

class RacesSchema(ma.Schema):
  class Meta:
    fields = ['race_id','race_name', 'homeland', 'lifespan']

  race_id = ma.fields.UUID(requird=True)
  race_name = ma.fields.String(requird=True)
  homeland = ma.fields.String(allow_none=True)
  lifespan =  ma.fields.Integer(allow_none=True)

race_schema = RacesSchema()
races_schema = RacesSchema(many=True)
