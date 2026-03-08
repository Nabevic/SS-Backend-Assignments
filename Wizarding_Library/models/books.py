import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Books(db.Model):
  __tablename__ = "Books"

  book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  school_id = db.Column(UUID(as_uuid=True), db.ForeignKey('MagicalSchools.school_id'),  nullable=False)
  title = db.Column(db.String(), nullable=False, unique=True)
  author = db.Column(db.String())
  subject = db.Column(db.String())
  rarity_level = db.Column(db.integer())
  magical_properties = db.Column(db.String())
  available = db.Column(db.Boolean(), default=True)

  magical_schools = db.relationship("MagicalSchools", foreign_keys='[Books.school_id]', back_populates='Books')


  def __init__(self, school_id, title, author, subject, rarity_level, magical_properties, availabe):
    self.school_id = school_id
    self.title = title
    self.author = author
    self.subject = subject
    self.rarity_level = rarity_level
    self.magical_properties = magical_properties
    self.available = availabe