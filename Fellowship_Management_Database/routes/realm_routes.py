from flask import Blueprint
import controllers


realm = Blueprint('realm', __name__)


@realm.route("/realm", methods=['POST'])
def add_realm():
  return controllers.add_realm()

@realm.route("/realm/<realm_id>", methods=['GET','PUT'])
def realm_by_id(realm_id):
  return controllers.realm_by_id(realm_id)

@realm.route("/realm/delete/<realm_id>", methods=['DELETE'])
def delete_realm(realm_id):
  return controllers.delete_realm(realm_id)