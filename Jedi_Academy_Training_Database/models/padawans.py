import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .padawan_courses_xref import padawan_course_enrollment_table

class Padawans(db.Model):
  __tablename__ = "Padawans"

  padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  master_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Masters.master_id'))
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
  species_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Species.species_id'), nullable=False)
  padawan_name = db.Column(db.String(), unique=True)
  age = db.Column(db.Integer())
  training_level = db.Column(db.Integer())
  graduation_date = db.Column(db.DateTime())

  master = db.relationship("Masters", foreign_keys='[Padawans.master_id]', back_populates='padawans')
  user = db.relationship("Users", foreign_keys='[Padawans.user_id]', back_populates='padawan')
  species = db.relationship("Species", foreign_keys='[Padawans.species_id]', back_populates='force_users')
  courses = db.relationship("Courses", secondary=padawan_course_enrollment_table, back_populates='padawans')

  def __init__(self, master_id, user_id, species_id, padawan_name, age, training_level, graduation_date):
    self.master_id = master_id
    self.user_id = user_id
    self.species_id = species_id
    self.padawan_name = padawan_name
    self.age = age
    self.training_level = training_level
    self.graduation_date = graduation_date

  def new_padawan_obj():
    return Padawans('','','','',0,0,'')
  
class PadawansSchema(ma.Schema):
  class Meta:
    fields = ['padawan_id', 'master_id', 'user_id', 'species_id', 'padawan_name', 'age', 'training_level', 'graduation_date', 'courses']

  padawan_id = ma.fields.UUID()
  master_id = ma.fields.UUID()
  user_id = ma.fields.UUID()
  species_id = ma.fields.UUID()
  padawan_name = ma.fields.String(required=True)
  age = ma.fields.Integer()
  training_level = ma.fields.Integer()
  graduation_date = ma.fields.DateTime()

  courses = ma.fields.Nested("CoursesSchema", many=True, only=['course_id', 'course_name', 'instructor_id'])

padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)