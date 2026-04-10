from flask import Blueprint
import controllers


temple = Blueprint('temple', __name__)

@temple.route('/temple', methods=['POST'])
def add_temple_route():
  return controllers.add_temple()

@temple.route('/temple/<temple_id>', methods=['GET'])
def get_temple_route(temple_id):
  return controllers.get_temple(temple_id)
  
@temple.route('/temple/<temple_id>', methods=['PUT'])
def update_temple_route(temple_id):
  return controllers.update_temple(temple_id)

@temple.route('/temple/delete/<temple_id>', methods=['DELETE'])
def delete_temple_route(temple_id):
  return controllers.delete_temple(temple_id)
