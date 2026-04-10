from db import db

padawan_course_enrollment_table = db.Table(
  "PadawanCourseEnrollment",
  db.Model.metadata,
  db.Column('padawan_id',db.ForeignKey('Padawans.padawan_id', ondelete='CASCADE'), primary_key=True),
  db.Column('course_id',db.ForeignKey('Courses.course_id', ondelete='CASCADE'), primary_key=True)
)