from flask import Blueprint
import controllers


lightsaber = Blueprint('lightsaber', __name__)

lightsaber.route('/lightsaber', methods=['Post'])
def add_lightsaber_route():
  return controllers.add_lightsaber()

lightsaber.route('/lightsaber/<owner_id>', methods=['GET'])
def get_lightsaber_route(owner_id):
  return controllers.get_lightsaber(owner_id)

lightsaber.route('/lightsaber/<saber_id>', methods=['PUT'])
def update_lightsaber(saber_id):
  return controllers.update_lightsaber(saber_id)

lightsaber.route('/lightsaber/delete/<saber_id>', methods=['DELETE'])
def delete_lightsaber_route(saber_id):
  return controllers.delete_lightsaber(saber_id)