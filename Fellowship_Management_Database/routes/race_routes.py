from flask import Blueprint
import controllers


race = Blueprint('race', __name__)


@race.route("/race", methods=['POST'])
def add_race():
  return controllers.add_race()

@race.route("/races", methods=['GET'])
def get_races():
  return controllers.get_races()

@race.route("/race/<race_id>", methods=['GET','PUT'])
def race_by_id(race_id):
  return controllers.race_by_id(race_id)

@race.route("/race/delete/<race_id>", methods=['POST'])
def delete_race(race_id):
  return controllers.delete_race(race_id)