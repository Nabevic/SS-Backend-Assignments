import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .padawan_courses_xref import padawan_course_enrollment_table

class Courses(db.Model):
  __tablename__ = "Courses"

  course_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Masters.master_id'), nullable=False)
  course_name = db.Column(db.String(), unique=True)
  difficulty = db.Column(db.String())
  duration_weeks = db.Column(db.Integer())
  max_students = db.Column(db.Integer())

  master = db.relationship("Masters", foreign_keys='[Courses.instructor_id]', back_populates='courses_teaching')
  padawans = db.relationship("Padawans", secondary=padawan_course_enrollment_table, back_populates='courses')

  def __init__(self, instructor_id, course_name, difficulty, duration_weeks, max_students):
    self.instructor_id = instructor_id
    self.course_name = course_name
    self.difficulty = difficulty
    self.duration_weeks = duration_weeks
    self.max_students = max_students

  def new_course_obj():
    return Courses('', '', '', 0, 0)


class CoursesSchema(ma.Schema):
  class Meta:
    fields = ['course_id', 'instructor_id', 'course_name', 'difficulty', 'duration_weeks', 'max_students', 'master', 'padawans']

  course_id = ma.fields.UUID()
  instructor_id = ma.fields.UUID(required=True)
  course_name = ma.fields.String(required=True)
  difficulty = ma.fields.String(allow_none=True)
  duration_weeks = ma.fields.Integer(allow_none=True)
  max_students = ma.fields.Integer(allow_none=True)

  master = ma.fields.Nested("MastersSchema", exclude=['courses_teaching'])
  padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['courses'])

course_schema = CoursesSchema()
courses_schema = CoursesSchema(many=True)