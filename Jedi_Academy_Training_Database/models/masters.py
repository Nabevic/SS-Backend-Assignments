import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Masters(ma.Schema):
  __tablename__ = 'Masters'

  master_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
  master_name = db.Column(db.String(), unique=True)
  specialization = db.Column(db.String())
  years_training = db.Column(db.Integer())
  max_padawans = db.Column(db.Integer())

  user = db.relationship("Users", foreign_keys='[Users.user_id]', back_populates='master')

  def __init__(self, user_id, master_name, specialization, years_training, max_padawans):
    
    self.user_id = user_id 
    self.master_name = master_name
    self.specialization = specialization
    self.years_training = years_training
    self.max_padawans = max_padawans

  def new_master_obj():
    return Masters('','','',0,0)
  
class MastersSchema(ma.Schema):
  class Meta:
    fields = ['master_id', 'user_id', 'master_name', 'specialization', 'years_training', 'max_padawans']

  master_id = ma.fields.UUID()
  user_id = ma.fields.UUID(required=True)
  master_name = ma.fields.String()
  specialization = ma.fields.String(allow_none=True)
  years_training = ma.fields.Integer(allow_none=True)
  max_padawans = ma.fields.Integer(allow_none=True)

master_schema = MastersSchema()
masters_schema = MastersSchema(many=True)