from flask import Blueprint
import controllers

warranty = Blueprint('warranty', __name__)


@warranty.route("/warranty", methods=['POST'])
def add_warranty():
  return controllers.add_warranty()


@warranty.route("/warranty/<warranty_id>", methods=['POST'])
def get_warranty_by_id(warranty_id):
  return controllers.get_warranty_by_id(warranty_id)


@warranty.route("/warranty/<warranty_id>", methods=["PUT"])
def update_warranty(warranty_id):
  return controllers.update_warranty(warranty_id)


@warranty.route('/warrany/delete/<warranty_id>', methods=['DELETE'])
def delete_warranty(warranty_id):
    return controllers.delete_warranty(warranty_id)