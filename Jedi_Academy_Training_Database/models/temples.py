import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Temples(db.Model):
  __tablename__ = "Temples"

  temple_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  temple_name = db.Column(db.String(), unique=True, nullable=False)
  planet = db.Column(db.String())
  master_count = db.Column(db.Integer())
  padawan_limit = db.Column(db.Integer())
  is_active = db.Column(db.Boolean(), default=True)

  user = db.relationship('Users', foreign_keys='[Users.temple_id]', back_populates='temple')

  def __init__(self, temple_name, planet, master_count, padawan_limit, is_active):
    self.temple_name = temple_name
    self.planet = planet
    self.master_count = master_count
    self.padawan_limit = padawan_limit
    self.is_active = is_active

  def new_temple_obj():
    return Temples('','',0,0,True)
  
class TemplesSchema(ma.Schema):
  class Meta:
    fields = ['temple_id', 'temple_name', 'planet', 'master_count', 'padawan_limit', 'is_active']

  temple_id = ma.fields.UUID()
  temple_name = ma.fields.String(required=True)
  planet = ma.fields.String()
  master_count = ma.fields.Integer()
  padawan_limit = ma.fields.Integer()
  is_active = ma.fields.Boolean(dump_default=True)
  
temple_schema = TemplesSchema()
temples_schema = TemplesSchema(many=True)