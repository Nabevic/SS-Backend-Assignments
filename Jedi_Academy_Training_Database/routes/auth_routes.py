from flask import Blueprint
import controllers


auth = Blueprint('auth', __name__)


auth.route('/user/auth', methods=['POST'])
def add_auth_token_route():
  controllers.add_auth_token()

