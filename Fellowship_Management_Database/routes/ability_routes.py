from flask import Blueprint
import controllers


ability = Blueprint('ability', __name__)


@ability.route("/ability", methods=['POST'])
def add_ability():
  return controllers.add_ability()

@ability.route("/ability/<ability_id>", methods=['PUT'])
def update_ability(ability_id):
  return controllers.update_ability(ability_id)

@ability.route("/ability/<ability_id>", methods=['DELETE'])
def delete_ability(ability_id):
  return controllers.delete_ability(ability_id)