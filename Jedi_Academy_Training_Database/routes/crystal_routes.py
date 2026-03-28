from flask import Blueprint
import controllers


crystal = Blueprint('crystal', __name__)

crystal.route('/crystal', methods=['POST'])
def add_crystal():
  return controllers.add_crystal()

crystal.route('crystals/<rarity_level>', methods=['GET'])
def get_crystal_by_rarity(rarity_level):
  return controllers.get_crystal_by_rarity(rarity_level)
