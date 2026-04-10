from flask import Blueprint
import controllers


course = Blueprint('course', __name__)

@course.route('/course', methods= ['POST'])
def add_course_route():
  return controllers.add_course()

@course.route('/enrollment', methods=['POST'])
def enroll_padawan_route():
  controllers.enroll_padawan()

@course.route('/courses/<difficulty_level>', methods= ['GET'])
def get_course_route(difficulty_level):
  return controllers.get_course(difficulty_level)

@course.route('/course/<course_id>', methods= ['PUT'])
def update_course_route(course_id):
  return controllers.update_course(course_id)

@course.route('/course/delete/<course_id>', methods= ['DELETE'])
def delete_course_route(course_id):
  return controllers.delete_course(course_id)

@course.route('/enrollment/<padawan_id>/<course_id>', methods=['DELETE'])
def remove_padawan_enrollment_route(padawan_id, course_id):
  return controllers.remove_padawan_enrollment(padawan_id, course_id)