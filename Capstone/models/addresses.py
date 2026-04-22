import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Addresses(db.Model):
  __tablename__ = 'Addresses'

  address_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  address_1 = db.Column(db.String(), nullable=False)
  address_2 = db.Column(db.String())
  address_3 = db.Column(db.String())
  city = db.Column(db.String(), nullable=False)
  state = db.Column(db.String(), nullable=False)
  postal_code = db.Column(db.String(), nullable=False)

  user = db.relationship("Users", foreign_keys='[Users.user_address]', back_populates='address')
  event = db.relationship("Events", foreign_keys='[Events.event_address]', cascade='all', back_populates='address')

  def __init__(self, address_1, address_2, address_3, city, state, postal_code):
    self.address_1 = address_1
    self.address_2 = address_2
    self.address_3 = address_3
    self.city = city
    self.state = state
    self.postal_code = postal_code 
  
  def new_address_obj():
    return Addresses('','','','','','')
  

class AddressesSchema(ma.Schema):
  class Meta:
    fields = ['address_id', 'address_1', 'address_2', 'address_3', 'city', 'state', 'postal_code']

  address_id = ma.fields.UUID()
  address_1 = ma.fields.String(required=True)
  address_2 = ma.fields.String()
  address_3 = ma.fields.String()
  city = ma.fields.String(required=True)
  state = ma.fields.String(required=True)
  postal_code = ma.fields.String(required=True)

address_schema = AddressesSchema()
addresses_schema = AddressesSchema(many=True)
