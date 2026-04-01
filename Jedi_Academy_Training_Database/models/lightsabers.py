import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Lightsabers(db.Model):
  __tablename__ = 'Lightsabers'
  
  saber_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
  crystal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Crystals.crystal_id"), nullable=False)
  saber_name = db.Column(db.String(), unique=True)
  hilt_material = db.Column(db.String())
  blade_color = db.Column(db.String())
  is_completed = db.Column(db.Boolean())

  owner = db.relationship("Users", foreign_keys='[Users.user_id]', back_populates='lightsaber')
  crystal = db.relationship("Crystals", foreign_keys='[Crystals.crystal_id]', back_populates='lightsaber')

  def __init__(self, owner_id, crystal_id, saber_name, hilt_material, blade_color, is_completed):
    self.owner_id = owner_id
    self.crystal_id = crystal_id
    self.saber_name = saber_name
    self.hilt_material = hilt_material
    self.blade_color = blade_color
    self.is_completed = is_completed

  def new_saber_obj():
    return Lightsabers('','','','','', False)
  

class LightsabersSchema(ma.Schema):
  class Meta:
    fields = [ 'owner', 'crystal', 'saber_name', 'hilt_material', 'blade_color', 'is_completed']

    saber_name = ma.fields.String(allow_none=True)
    hilt_material = ma.fields.String(allow_none=True)
    blade_color = ma.fields.String(allow_none=True)
    is_completed = ma.fields.Boolean(allow_none=True)

    owner = ma.fields.Nested("UsersSchema", only=['user_id', 'username', 'force_rank', 'midi_count', 'is_active'])
    crystal = ma.fields.Nested("Crystals")


lightsaber_schema = LightsabersSchema()
lightsabers_schema = LightsabersSchema(many=True)
