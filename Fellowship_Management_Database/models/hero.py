import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .hero_quest_xref import hero_quest_association_table


class Heroes(db.Model):
  __tablename__ = "Heroes"

  hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  race_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Races.race_id"), nullable=False)
  hero_name = db.Column(db.String(), unique=True, nullable=False)
  age = db.Column(db.Integer())
  health_points = db.Column(db.Integer())
  is_alive = db.Column(db.Boolean(), default=True)

  race = db.relationship("Races", foreign_keys='[Heroes.race_id]', back_populates='heroes', cascade='all')
  abilities = db.relationship("Abilities", foreign_keys='[Abilities.hero_id]', back_populates='hero', uselist=False, cascade='all')
  quests = db.relationship("Quests", secondary=hero_quest_association_table, back_populates='heroes')

  def __init__(self, race_id, hero_name, age, health_points, is_alive):
    self.race_id = race_id
    self.hero_name = hero_name
    self.age = age
    self.health_points = health_points
    self.is_alive = is_alive

  def new_hero_obj():
    return Heroes('', '', 0, 0, True)
  

class HeroesSchema(ma.Schema):
  class Meta:
    fields = ['hero_id', 'hero_name', 'age', 'health_points', 'is_alive', 'race' ]

  hero_id = ma.fields.UUID()
  hero_name = ma.fields.String(required=True)
  age = ma.fields.Integer(allow_none=True)
  health_points = ma.fields.Integer(required=True)
  is_alive = ma.fields.Boolean(dump_default=True)
  race = ma.fields.Nested("RacesSchema", only=['race_id', 'race_name'])
  

hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)

class HeroDetailsSchema(HeroesSchema):
  class Meta:
    fields = ['hero_id', 'hero_name', 'age', 'health_points', 'is_alive', 'race', 'abilities', 'quests' ]

  race = ma.fields.Nested("RacesSchema")
  abilities = ma.fields.Nested("AbilitiesSchema")
  quests = ma.fields.Nested("QuestsSchema", many=True)

hero_details_schema = HeroDetailsSchema()