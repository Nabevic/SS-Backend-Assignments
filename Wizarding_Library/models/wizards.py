import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.wizard_specializations import wizard_specializations_table


class Wizards(db.Model):
  __tablename__ = "Wizards"

  wizard_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  school_id = db.Column(UUID(as_uuid=True), db.ForeignKey("MagicalSchools.school_id"), nullable=False)
  wizard_name = db.Column(db.String(), nullable=False, unique=True)
  house = db.Column(db.String())
  year_enrolled = db.Column(db.Integer())
  magical_power_level = db.Column(db.Integer())
  active = db.Column(db.Boolean(), default=True)

  schools = db.relationship("MagicalSchools", foreign_keys='[Wizards.school_id]', back_populates='wizards')
  spells = db.relationship("Spells", secondary=wizard_specializations_table, back_populates = 'wizards')

  def __init__(self, school_id, wizard_name, house, year_enrolled, magical_power_level, active):
    self.school_id = school_id
    self.wizard_name = wizard_name
    self.house = house
    self.year_enrolled = year_enrolled
    self.magical_power_level = magical_power_level
    self.active = active