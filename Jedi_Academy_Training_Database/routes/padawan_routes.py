from flask import Blueprint
import controllers


padawan = Blueprint('padawan', __name__)

@padawan.route('/padawan', methods=['POST'])
def add_padawan_route():
  return controllers.add_padawan()

@padawan.route('/padawans', methods=['GET'])
def get_all_padawans_route():
  return controllers.get_all_padawans()

@padawan.route('/padawans/active', methods=['GET'])
def get_active_padawans_route():
  return controllers.get_active_padawans()

@padawan.route('/padawan/<padawan_id>', methods=['PUT'])
def update_padawan_route(padawan_id):
  return controllers.update_padawan(padawan_id)

@padawan.route('/padawan/<padawan_id>/promote', methods=['PUT'])
def promote_padawan_route(padawan_id):
  return controllers.promote_padawan(padawan_id)

@padawan.route('/padawan/delete/<padawan_id>', methods=['DELETE'])
def delete_padawan_route(padawan_id):
  return controllers.delete_padawan(padawan_id)


