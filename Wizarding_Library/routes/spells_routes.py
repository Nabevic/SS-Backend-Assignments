from flask import Blueprint
import controllers


spell = Blueprint('spell', __name__)


@spell.route('/spell', methods=['POST'])
def add_spell():
  return controllers.add_spell()

@spell.route('/spells', methods=['GET'])
def get_spells():
  return controllers.get_spells()

@spell.route('/spells/<difficulty_level>', methods=['GET'])
def get_spells_by_difficulty(difficulty_level):
  return controllers.get_spell_by_difficulty(difficulty_level)

@spell.route('/spell/<spell_id>', methods=['PUT'])
def update_spell(spell_id):
  return controllers.update_spell(spell_id)

@spell.route('/spell/delete/<spell_id>', methods=['DELETE'])
def delete_spell(spell_id):
  return controllers.delete_spell(spell_id)