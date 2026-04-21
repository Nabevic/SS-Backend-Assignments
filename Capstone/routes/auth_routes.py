from flask import Blueprint
import controllers


auth = Blueprint('auth', __name__)


@auth.route('/user/auth', methods=['POST'])
def add_auth_token_route():
  return controllers.add_auth_token()

@auth.route('/logout', methods=['DELETE'])
def delete_auth_token_route():
  return controllers.delete_auth_token()
