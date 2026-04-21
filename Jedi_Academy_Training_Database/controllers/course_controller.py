from flask import jsonify, request

from db import db
from models.courses import Courses, course_schema, courses_schema
from models.padawans import Padawans
from models.masters import Masters
from lib.authenticate import authenticate_return_auth, clearance
from util.reflection import populate_object



@authenticate_return_auth #Master+ rank
def add_course(auth_info):
  if auth_info.user.force_rank in clearance['Master']:
    post_data = request.form if request.form else request.get_json()
    master_query = db.session.query(Masters).filter(Masters.master_id == post_data['instructor_id']).first()
    if not master_query:
      return jsonify({"message": f"unable to add course. Master with id {post_data['instructor_id']} does not exist"}), 400

    new_course = Courses.new_course_obj()
    populate_object(new_course, post_data)
    try:
      db.session.add(new_course)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add course. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "course added", "result": course_schema.dump(new_course)}), 201
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Master+ rank
def enroll_padawan(auth_info):
  if auth_info.user.force_rank not in clearance['Master']:
    return jsonify({"message": "unauthorized"}), 401
  else:  
    post_data = request.form if request.form else request.get_json()
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == post_data['padawan_id']).first()
    course_query = db.session.query(Courses).filter(Courses.course_id == post_data['course_id']).first()

  if not padawan_query:
    return jsonify({"message":"unable to complete enrollment, padawan not found"}), 404
  
  if not course_query:
    return jsonify({"message":"unable to complete enrollment, course not found"}), 404
  
  for padawan in course_query.padawans:
    if padawan.padawan_id == post_data["padawan_id"]:
      return jsonify({"message":"unable to complete enrollment, padawan already enrolled in course"}), 400

  try:
    course_query.padawans.append(padawan_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to complete enrollment. {e}"}), 400

  db.session.commit()
  return jsonify({"message": "padawan successfuly enrolled in course", "result": course_schema.dump(course_query)}), 201  



@authenticate_return_auth
def get_course(difficulty, auth_info):
  if auth_info.user.force_rank in clearance['Basic']:
    course_query = db.session.query(Courses).filter(Courses.difficulty == difficulty).all()

    if not course_query:
      return jsonify({"message": "no courses found"}), 404

    return jsonify({"message": "courses retrieved", "results": courses_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Instructor or Council+ 
def update_course(course_id, auth_info):
  course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
  if not course_query:
    return jsonify({"message": "unable to update record, course not found"}), 404
  
  if auth_info.user.user_id == course_query.instructor_id or auth_info.user.force_rank in clearance['Council']:
    post_data = request.form if request.form else request.get_json()

    populate_object(course_query, post_data)
    db.session.commit()

    return jsonify({"message": "course updated", "results": course_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401



@authenticate_return_auth #Instructor or Council+
def delete_course(course_id, auth_info):
  course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
  if not course_query:
    return jsonify({"message": f"no course found with id {course_id}"}), 404
  
  if auth_info.user.user_id == course_query.instructor_id or auth_info.user.force_rank in clearance['Council']:
    try:
      db.session.delete(course_query)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "course deleted", "result": course_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401

  

@authenticate_return_auth
def remove_padawan_enrollment(padawan_id, course_id, auth_info):
  if auth_info.user.force_rank in clearance['Basic']:
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    enrollment_query = db.session.query(Courses).filter(Courses.course_id == course_id and Courses.padawans.padawan_id == padawan_id).first()
    if not padawan_query:
      return jsonify({"message":"unable to remove padawan from course, padawan id invalid"}), 404
    
    elif not course_query:
      return jsonify({"message":"unable to remove padawan from course, course id invalid"}), 404

    if not enrollment_query:
      return jsonify({"message":"unable to remove padawan from course, padawan isn't enrolled."}), 400

    try:
      course_query.padawans.remove(padawan_query)
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to remove enrollment. {e}"}), 400
    
    db.session.commit()
    return jsonify({"message": "enrollment removed", "result": course_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401