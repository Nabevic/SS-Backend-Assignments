import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .board_games_categories_xref import games_categories_association_table

class Categories(db.Model):
  __tablename__ = "Categories"

  category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  category_name = db.Column(db.String(), nullable=False, unique=True)

  board_games = db.relationship("BoardGames", secondary=games_categories_association_table, back_populates='categories')

  def __init__(self, category_name):
    self.category_name = category_name

  def new_category_obj():
    return Categories('')
  
class CategoriesSchema(ma.Schema):
  class Meta:
    fields = ['category_id', 'category_name']

  category_id = ma.fields.UUID()
  category_name = ma.fields.String(required=True)

category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)