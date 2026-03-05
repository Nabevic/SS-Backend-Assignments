from flask import Blueprint
import controllers

magical_school = Blueprint('magical_school', __name__)

@magical_school.route('/school', methods=['POST'])
def add_school():
  return controllers.add_school()

@magical_school.route('/schools', methods=['GET'])
def get_schools():
  return controllers.get_schools()

@magical_school.route('/school/<school_id>', methods=['GET','PUT'])
def school_by_id(school_id):
  return controllers.school_by_id(school_id)

@magical_school.route('/school/delete/<school_id>', methods=['DELETE'])
def delete_school(school_id):
  return controllers.delete_school(school_id)
