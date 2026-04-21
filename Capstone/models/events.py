import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Events(db.Model):
  __tablename__ = 'Events'

  event_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  host = db.Column(UUID(as_uuid=True), db.ForiegnKey('Users.user_id'))
  location = db.Column(UUID(as_uuid=True), db.ForiegnKey('Addresses.Address_id'))
  date = db.Column(db.DateTime())
  notes = db.Column(db.String())

  host = db.relationship("Users", foreign_keys='[Users.user_id]', back_populates='event')
  location = db.relationship("Addresses", foreign_keys='Addresses.address_id', back_populates='event')


  def _init__(self, host, location, date, notes):
    self.host = host
    self.location = location
    self.date = date
    self.notes = notes

  def new_event_obj():
    return Events('','','','','')
  

class EventsSchema(ma.Schema):
  class Meta:
    fields = ['event_id', 'host', 'location', 'date', 'notes']

  event_id = ma.fields.UUID()
  date = ma.fields.DateTime(required=True)
  notes = ma.fields.String(allow_none=True)

  host = ma.fields.Nested("UsersSchema", only=['user_id', 'first_name', 'last_name', 'phone'])
  location = ma.fields.Nested("AddressesSchema")

event_schema = EventsSchema()
events_schema = EventsSchema(many=True)