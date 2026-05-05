from flask import Blueprint

import controllers


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
def add_user_route():
  return controllers.add_user()

@user.route('/users', methods=['GET'])
def get_all_users_route():
  return controllers.get_all_users()

@user.route('/users/active', methods=['GET'])
def get_active_users_route():
  return controllers.get_active_users()

@user.route('/user/profile', methods=['GET'])
def get_user_profile_route():
  return controllers.get_user_profile()

@user.route('/user/<user_id>', methods=['GET','PUT'])
def user_by_id(user_id):
  return controllers.user_by_id(user_id)

@user.route('/user/activation', methods=['PUT'])
def user_activation_route():
  return controllers.user_activation_route()

@user.route('/user/delete', methods=['DELETE'])
def delete_user():
  return controllers.delete_user()