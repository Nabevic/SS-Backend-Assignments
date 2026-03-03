from flask import Blueprint

import controllers

product = Blueprint('product', __name__)

@product.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    return controllers.update_product_by_id(product_id)
