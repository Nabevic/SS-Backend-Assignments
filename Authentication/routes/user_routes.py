from flask import Blueprint

import controllers


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
def add_user_route():
  return controllers.add_user()

@user.route('/users', methods=['GET'])
def get_all_users_route():
  return controllers.get_all_users()

@user.route('/user/<user_id>', methods=['GET','PUT'])
def user_by_id(user_id):
  return controllers.user_by_id(user_id)

@user.route('/user/delete', methods=['DELETE'])
def delete_user():
  return controllers.delete_user()