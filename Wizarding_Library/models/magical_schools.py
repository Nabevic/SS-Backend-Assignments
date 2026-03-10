import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class MagicalSchools(db.Model):
  __tablename__ = "MagicalSchools"

  school_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  school_name = db.Column(db.String(), nullable=False, unique=True)
  location = db.Column(db.String())
  founded_year = db.Column(db.Integer())
  headmaster = db.Column(db.String())

  books = db.relationship("Books", foreign_keys='[Books.school_id]', back_populates="magical_schools", uselist=False, cascade='all')
  wizards = db.relationship("Wizards", foreign_keys='[Wizards.school_id]', back_populates='schools', cascade='all')

  def __init__(self, school_name, location, founded_year, headmaster):
    self.school_name = school_name
    self.location = location
    self.founded_year = founded_year
    self.headmaster = headmaster
