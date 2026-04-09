import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Realms(db.Model):
  __tablename__ = "Realms"

  realm_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  realm_name = db.Column(db.String(), unique=True, nullable=False)
  ruler = db.Column(db.String())

  locations = db.relationship("Locations", foreign_keys='[Locations.realm_id]', back_populates='realm', cascade='all')

  def __init__(self, realm_name, ruler):
    self.realm_name = realm_name
    self.ruler = ruler

  def new_realm_obj():
    return Realms('','')
  

class RealmsSchema(ma.Schema):
  class Meta:
    fields = ['realm_id', 'realm_name', 'ruler']

  realm_id = ma.fields.UUID()
  realm_name = ma.fields.String(required=True)
  ruler = ma.fields.String()

realm_schema = RealmsSchema()
realms_schema = RealmsSchema(many=True)

class RealmDetailsSchema(RealmsSchema):
  class Meta:
    fields = ['realm_id', 'realm_name', 'ruler', 'locations']

  locations = ma.fields.Nested("LocationsSchema", many=True, exclude=['realm_id'])

realm_details_schema = RealmDetailsSchema()


