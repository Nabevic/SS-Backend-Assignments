import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Crystals(db.Model):
  __tablename__ = "Crystals"

  crystal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  crystal_type = db.Column(db.String(), unique=True)
  origin_planet = db.Column(db.String())
  rarity_level = db.Column(db.String())
  force_amplify = db.Column(db.Float())

  lightsaber = db.relationship("Lightsabers", foreign_keys='[Lightsabers.saber_id]', back_populates='crystal', cascade='all')

  def __init__(self, crystal_type, origin_planet, rarity_level, force_amplify):
    self.crystal_type = crystal_type
    self.origin_planet = origin_planet
    self.rarity_level = rarity_level
    self.force_amplify = force_amplify

  def new_crystal_obj():
    return Crystals('', '', '', 0)
  

class CrystalsSchema(ma.Schema):
  class Meta:
    fields = ['crystal_id','crystal_type', 'origin_planet', 'rarity_level', 'force_amplify']

    crystal_id = ma.fields.UUID()
    crystal_type = ma.fields.String(allow_none=True)
    origin_planet = ma.fields.String(allow_none=True)
    rarity_level = ma.fields.String(allow_none=True)
    force_amplify = ma.fields.Float(allow_none=True)

crystal_schema = CrystalsSchema()
crystals_schema = CrystalsSchema(many=True)