from flask import Blueprint
import controllers


lightsaber = Blueprint('lightsaber', __name__)

lightsaber.route('/lightsaber', methods=['Post'])
def add_lightsaber_route():
  return controllers.add_lightsaber()

lightsaber.route('/lightsaber/<owner_id>', methods=['GET'])
def get_lightsaber_route(owner_id):
  return controllers.get_lightsaber(owner_id)

lightsaber.route('/lightsaber/<lightsaber_id>', methods=['PUT'])
def update_lightsaber_route(lightsaber_id):
  return controllers.update_lightsaber(lightsaber_id)

lightsaber.route('/lightsaber/delete/<lightsaber_id>', methods=['DELETE'])
def delete_lightsaber_route(lightsaber_id):
  return controllers.delete_lightsaber(lightsaber_id)