import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Users(db.Model):
  __tablename__ = 'Users'

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Temples.temple_id'))
  username = db.Column(db.String(), nullable=False, unique=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  force_rank = db.Column(db.String())
  midi_count = db.Column(db.Integer())
  joined_date = db.Column(db.DateTime(), nullable=False)
  is_active = db.Column(db.Boolean(), nullable=False, default=True)

  auth = db.relationship('AuthTokens', back_populates='user', cascade='all' )
  master = db.relationship('Masters', foreign_keys='[Masters.user_id]', back_populates='user')
  padawan = db.relationship('Padawans', foreign_keys='[Padawans.user_id]', back_populates='user')
  temple = db.relationship('Temples', foreign_keys='[Users.temple_id]', back_populates='user')
  lightsaber = db.relationship('Lightsabers', foreign_keys='[Lightsabers.owner_id]', back_populates='owner')


  def __init__(self, temple_id, username, email, password, force_rank, midi_count, joined_date, is_active=True):
    self.temple_id = temple_id
    self.username = username
    self.email = email
    self.password = password
    self.force_rank = force_rank
    self.midi_count = midi_count
    self.joined_date = joined_date
    self.is_active = is_active


  def new_user_obj():
    return Users('','','','','',0,'',True,)
  

class UsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id','temple_id', 'username', 'email', 'force_rank', 'midi_count', 'joined_date', 'is_active']

  user_id = ma.fields.UUID()
  temple_id = ma.fields.UUID()
  username = ma.fields.String(required=True)
  email = ma.fields.String(required=True)
  force_rank = ma.fields.String()
  midi_count = ma.fields.Integer(allow_none=True)
  joined_date = ma.fields.String(required=True,)
  is_active = ma.fields.Boolean(required=True, dump_default=True)


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)