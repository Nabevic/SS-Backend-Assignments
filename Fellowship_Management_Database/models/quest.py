import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .hero_quest_xref import hero_quest_association_table


class Quests(db.Model):
  __tablename__ = "Quests"

  quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  location_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Locations.location_id"), nullable=False)
  quest_name = db.Column(db.String(), unique=True, nullable=False)
  difficulty_level = db.Column(db.String())
  reward_gold = db.Column(db.Integer())
  is_completed = db.Column(db.Boolean(), default=False)

  heroes = db.relationship("Heroes", secondary=hero_quest_association_table, back_populates="quests")
  location = db.relationship("Locations", foreign_keys='[Quests.location_id]', back_populates='quests')

  def __init__(self, location_id, quest_name, difficulty_level, reward_gold, is_completed):
    self.location_id = location_id
    self.quest_name = quest_name
    self.difficulty_level = difficulty_level
    self.reward_gold = reward_gold
    self.is_completed = is_completed

  def new_quest_obj():
    return Quests('', '', '', 0, False)
  

class QuestsSchema(ma.Schema):
  class Meta:
    fields = ['quest_id', 'quest_name', 'difficulty_level', 'reward_gold', 'is_completed', 'location_id']

  quest_id = ma.fields.UUID(required=True)
  location_id = ma.fields.UUID(required=True)
  quest_name = ma.fields.String(required=True)
  difficulty_level = ma.fields.String(allow_none=True)
  reward_gold = ma.fields.Integer(allow_none=True)
  is_completed = ma.fields.Boolean(dump_default=False)

quest_schema = QuestsSchema()
quests_schema = QuestsSchema(many=True)

class QuestDetailsSchema(QuestsSchema):
  class Meta:
    fields = ['quest_id', 'quest_name', 'difficulty_level', 'reward_gold', 'is_completed', 'location', 'heroes']
  location = ma.fields.Nested("LocationsSchema")
  heroes = ma.fields.Nested("HeroesSchema", many=True, only=['hero_id', 'hero_name'])

quest_details_schema = QuestDetailsSchema()