from flask import Blueprint
import controllers


hero = Blueprint('hero', __name__)


@hero.route("/hero", methods=['POST'])
def add_hero():
  return controllers.add_hero()

@hero.route("/hero-quest", methods=['POST'])
def add_hero_quest():
  return controllers.add_hero_quest()

@hero.route("/heroes", methods=['GET'])
def get_heroes():
  return controllers.get_heroes()

@hero.route("/heroes/alive", methods=['GET'])
def get_heroes_alive():
  return controllers.get_heroes_alive()

@hero.route("/hero/<hero_id>/quests", methods=['GET'])
def get_hero_quests(hero_id):
  return controllers.get_hero_quests(hero_id)

@hero.route("/hero/<hero_id>", methods=['GET','PUT'])
def hero_by_id(hero_id):
  return controllers.hero_by_id(hero_id)

@hero.route("/hero/delete/<hero_id>", methods=['DELETE'])
def delete_hero(hero_id):
  return controllers.delete_hero(hero_id)