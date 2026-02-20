from flask import Flask, jsonify, request

from db import db
from models.products import Products
from models.categories import Categories

def product_by_id(product_id):
  query = db.session.query(Products).filter(Products.product_id == product_id).first()
  if not query:
      return jsonify({"message": f"product does not exist"}), 400

  categories_list = []

  for category in query.categories:
      categories_list.append({
          "category_id": category.category_id,
          "category_name": category.category_name
      })

  company_record = {
      'company_id': query.companies.company_id,
      'company_name': query.companies.company_name
  }

  if query.warranty:
      warranty_record = {
          'warranty_id': query.warranty.warranty_id,
          'warranty_months': query.warranty.warranty_months
      }
  else:
      warranty_record = {}

  product_record = {
      'product_id': query.product_id,
      'product_name': query.product_name,
      'description': query.description,
      'price': query.price,
      'active': query.active,
      'company': company_record,
      'warranty': warranty_record,
      'categories': categories_list,
  }

  return jsonify({"message": "product found", "result": product_record}), 200
