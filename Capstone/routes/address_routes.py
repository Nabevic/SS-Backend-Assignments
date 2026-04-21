from flask import Blueprint

import controllers


address = Blueprint('address', __name__)


@address.route('/address', methods=['POST'])
def add_address_route():
  return controllers.add_address()

@address.route('/addresses', methods=['GET'])
def get_all_addresses_route():
  return controllers.get_all_addresses()

@address.route('/address/<address_id>', methods=['GET','PUT'])
def address_by_id_route(address_id):
  return controllers.address_by_id(address_id)

@address.route('/address', methods=['DELETE'])
def delete_address_route():
  return controllers.delete_address()