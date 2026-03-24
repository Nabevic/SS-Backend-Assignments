import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db



class Abilities(db.Model):
  __tablename__ = "Abilities"

  ability_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  hero_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Heroes.hero_id"), nullable=False)
  ability_name = db.Column(db.String(), unique=True, nullable=False)
  power_level = db.Column(db.Integer())

  hero = db.relationship("Heroes", foreign_keys='[Abilities.hero_id]', back_populates='abilities', uselist=False)
 


  def __init__(self,hero_id, ability_name, power_level):
    self.hero_id = hero_id
    self.ability_name = ability_name
    self.power_level = power_level

  def new_ability_obj():
    return Abilities('', '', 0)
  
class AbilitiesSchema(ma.Schema):
  class Meta:
    fields = ['ability_id', 'hero_id', 'ability_name', 'power_level']

  ability_id = ma.fields.UUID()
  hero_id = ma.fields.UUID(required=True)
  ability_name = ma.fields.String(required=True)
  power_level = ma.fields.Integer(required=True)


ability_schema = AbilitiesSchema()
abilities_schema = AbilitiesSchema(many=True)





