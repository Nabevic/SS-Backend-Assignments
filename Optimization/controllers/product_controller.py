from flask import jsonify, request

from db import db
from models.product import Products, product_schema, products_schema
from util.reflection import populate_object

# CREATE



# READ



# UPDATE

def update_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    post_data = request.form if request.form else request.get_json()

    if product_query:
        populate_object(product_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "product found", "results": product_schema.dump(product_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

