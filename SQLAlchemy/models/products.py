import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.companies import Companies
from models.products_categories_xref import products_categories_association_table


class Products(db.Model):
  __tablename__ = "Products"

  product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)
  product_name = db.Column(db.String(), nullable=False)
  price = db.Column(db.Float(),nullable=False)
  description = db.Column(db.String())
  active = db.Column(db.Boolean(), default=True)

  company = db.relationship("Companies", foreign_keys='[Products.company_id]', back_populates='products')
  category = db.relationship("Categories", secondary=products_categories_association_table, back_populates = 'products')
  db.relationship("warranties",foreign_keys = '[Warranties.product_id]', back_populates = 'products', uselist=False, cascade='all')


  def __init__(self,company_id, product_name, price, description, active=True):
    self.company_id = company_id
    self.product_name = product_name
    self.price = price
    self.description = description
    self.active = active