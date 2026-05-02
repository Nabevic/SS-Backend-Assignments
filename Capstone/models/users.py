import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Users(db.Model):
  __tablename__ = 'Users'

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_address = db.Column(UUID(as_uuid=True), db.ForeignKey("Addresses.address_id"))
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  birthdate = db.Column(db.DateTime(), nullable=False)
  phone = db.Column(db.String())
  role = db.Column(db.String(), nullable=False, default='user')
  active = db.Column(db.Boolean(), nullable=False, default=True)

  auth = db.relationship('AuthTokens', back_populates='user', cascade='all')
  address = db.relationship('Addresses', foreign_keys='[Users.user_address]', back_populates='user')
  event = db.relationship("Events", foreign_keys='[Events.host_id]', back_populates='host')
  borrower = db.relationship("GameLoans", foreign_keys='[GameLoans.borrower_id]', back_populates='user')

  def __init__(self, user_address, first_name, last_name, email, password, birthdate, phone, role, active):
    self.user_address = user_address
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.birthdate = birthdate
    self.phone = phone
    self.role = role
    self.active = active

  def new_user_obj():
    return Users(None,'','','','','','','user',True)
    

class UsersSchema(ma.Schema):
  class Meta:
    fields = [ 'user_id', 'user_address', 'first_name', 'last_name', 'email', 'birthdate', 'phone', 'role', 'active']

  user_id = ma.fields.UUID()
  user_address = ma.fields.UUID(allow_none=True)
  first_name = ma.fields.String(required=True)
  last_name = ma.fields.String(required=True)
  email = ma.fields.String(required=True)
  birthdate = ma.fields.DateTime(required=True)
  phone = ma.fields.String(allow_none=True)
  role = ma.fields.String(required=True, dump_default='user')
  active = ma.fields.Boolean(required=True, dump_default=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)