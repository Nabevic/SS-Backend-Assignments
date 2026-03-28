from flask import Blueprint
import controllers


padawan = Blueprint('padawan', __name__)

padawan.route('/padawan', methods=['POST'])
def add_padawan_route():
  controllers.add_padawan()



padawan.route('/padawans', methods=['GET'])
def get_all_padawans_route():
  controllers.get_all_padawans()

padawan.route('/padawans/active', methods=['GET'])
def get_active_padawans_route():
  controllers.get_active_padawans()

padawan.route('/padawan/<padawan_id>', methods=['PUT'])
def update_padawan_route(padawan_id):
  controllers.update_padawan(padawan_id)

padawan.route('/padawan/<padawan_id>/promote', methods=['PUT'])
def promote_padawan_route(padawan_id):
  controllers.promote_padawan(padawan_id)

padawan.route('/padawan/delete/<padawan_id>', methods=['DELETE'])
def delete_padawan_route(padawan_id):
  controllers.delete_padawan(padawan_id)



