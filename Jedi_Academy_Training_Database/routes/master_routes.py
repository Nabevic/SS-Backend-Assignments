from flask import Blueprint
import controllers


master = Blueprint('master', __name__)


@master.route('/master', methods=['POST'])
def add_master_route():
  return controllers.add_master()

@master.route('/masters', methods=['GET'])
def get_all_masters_route():
  return controllers.get_all_masters()

@master.route('/master/<master_id>', methods=['PUT'])
def update_master_route(master_id):
  return controllers.update_master(master_id)
  
@master.route('/master/delete/<master_id>', methods=['DELETE'])
def delete_master_route(master_id):
  return controllers.delete_master(master_id)

