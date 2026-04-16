import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Species(db.Model):
  __tablename__ = "Species"

  species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  species_name = db.Column(db.String(), unique=True)
  homeworld = db.Column(db.String())
  force_sensitive = db.Column(db.Boolean())
  avg_lifespan = db.Column(db.Integer())

  force_users = db.relationship("Padawans", foreign_keys='[Padawans.species_id]', back_populates='species')

  def __init__(self, species_name, homeworld, force_sensitive, avg_lifespan):
    self.species_name = species_name
    self.homeworld = homeworld
    self.force_sensitive = force_sensitive
    self.avg_lifespan = avg_lifespan

  def new_species_obj():
    return Species('','',False,0)
  
class SpeciesSchema(ma.Schema):
  class Meta:
    fields =['species_id', 'species_name', 'homeworld', 'force_sensitive', 'avg_lifespan', 'force_users']

  species_id = ma.fields.UUID()
  species_name = ma.fields.String(required=True)
  homeworld = ma.fields.String()
  force_sensitive = ma.fields.Boolean()
  avg_lifespan = ma.fields.Integer()

  force_users = ma.fields.Nested("PadawansSchema", many=True, only=['padawan_id', 'padawan_name', 'age'])

species_schema = SpeciesSchema()
many_species_schema = SpeciesSchema(many=True)