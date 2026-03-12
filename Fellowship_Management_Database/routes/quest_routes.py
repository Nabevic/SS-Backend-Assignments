from flask import Blueprint
import controllers


quest = Blueprint('quest', __name__)


@quest.route("/quest", methods=['POST'])
def add_quest():
  return controllers.add_quest()

@quest.route("/quests/<difficulty_level>", methods=['GET'])
def get_quests_by_difficulty(difficulty_level):
  return controllers.get_quests_by_difficulty(difficulty_level)

@quest.route("/quest/<quest_id>", methods=['GET','PUT'])
def quest_by_id(quest_id):
  return controllers.quest_by_id(quest_id)

@quest.route("/quest/<quest_id>/complete", methods=['PATCH'])
def complete_quest(quest_id):
  return controllers.complete_quest(quest_id)

@quest.route("/quest/delete/<quest_id>", methods=['DELETE'])
def delete_quest(quest_id):
  return controllers.delete_quest(quest_id)