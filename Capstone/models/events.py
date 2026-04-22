import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Events(db.Model):
  __tablename__ = 'Events'

  event_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  host_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'))
  event_address = db.Column(UUID(as_uuid=True), db.ForeignKey('Addresses.address_id'))
  date = db.Column(db.DateTime())
  notes = db.Column(db.String())

  host = db.relationship("Users", foreign_keys='[Events.host_id]', back_populates='event')
  address = db.relationship("Addresses", foreign_keys='Events.event_address', back_populates='event')


  def _init__(self, host_id, event_address, date, notes):
    self.host_id = host_id
    self.event_address = event_address
    self.date = date
    self.notes = notes

  def new_event_obj():
    return Events('','','','')
  

class EventsSchema(ma.Schema):
  class Meta:
    fields = ['event_id', 'host', 'address', 'date', 'notes']

  event_id = ma.fields.UUID()
  date = ma.fields.DateTime(required=True)
  notes = ma.fields.String(allow_none=True)

  host = ma.fields.Nested("UsersSchema", only=['user_id', 'first_name', 'last_name', 'phone'])
  address = ma.fields.Nested("AddressesSchema")

event_schema = EventsSchema()
events_schema = EventsSchema(many=True)