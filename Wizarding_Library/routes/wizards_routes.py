from flask import Blueprint
import controllers

wizard = Blueprint('wizard',__name__)


@wizard.route('/wizard', methods=['POST'])
def add_wizard():
  return controllers.add_wizard()

@wizard.route('/wizard/specialize', methods=['POST'])
def add_wizard_specialization():
  return controllers.add_wizard_specialization()

@wizard.route('/wizards', methods=['GET'])
def get_all_wizards():
  return controllers.get_all_wizards()

@wizard.route('/wizards/active', methods=['GET'])
def get_active_wizards():
  return controllers.get_active_wizards()

@wizard.route('/wizards/<house>', methods=['GET'])
def get_wizards_by_house(house):
  return controllers.get_wizards_by_house(house)

@wizard.route('/wizards/<magical_power_level>', methods=['GET'])
def get_wizards_by_power(magical_power_level):
  return controllers.get_wizards_by_power(magical_power_level)

@wizard.route('/wizard/<wizard_id>', methods=['GET','PUT'])
def wizard_id(wizard_id):
  return controllers.wizard_id(wizard_id)

@wizard.route('/wizard/delete/<wizard_id>', methods=['DELETE'])
def delete_wizard(wizard_id):
  return controllers.delete_wizard(wizard_id)

