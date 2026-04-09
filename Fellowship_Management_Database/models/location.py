import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Locations(db.Model):
  __tablename__ = "Locations"

  location_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  realm_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Realms.realm_id"), nullable=False)
  location_name = db.Column(db.String(), unique=True, nullable=False)
  danger_level = db.Column(db.Integer())
  

  realm = db.relationship("Realms", foreign_keys='[Locations.realm_id]', back_populates='locations')
  quests = db.relationship("Quests", foreign_keys='[Quests.location_id]', back_populates='location', cascade='all')

  def __init__(self, realm_id, location_name, danger_level):
    self.realm_id = realm_id
    self.location_name = location_name
    self.danger_level = danger_level

  def new_location_obj():
    return Locations('', '', 0)
  

class LocationsSchema(ma.Schema):
  class Meta:
    fields = ['location_id', 'realm_id', 'location_name', 'danger_level']

  location_id = ma.fields.UUID()
  realm_id = ma.fields.UUID(required=True)
  location_name = ma.fields.String(required=True)
  danger_level = ma.fields.Integer(allow_none=True)


location_schema = LocationsSchema()
locations_schema = LocationsSchema(many=True)

class LocationDetailsSchema(LocationsSchema):
  class Meta:
    fields = ['location_id','location_name', 'danger_level', 'realm', 'quests']

  realm = ma.fields.Nested("RealmsSchema")
  quests = ma.fields.Nested("QuestsSchema", many=True)

location_details_schema = LocationDetailsSchema()
