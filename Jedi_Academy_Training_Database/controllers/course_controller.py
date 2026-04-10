from flask import jsonify, request

from db import db
from models.courses import Courses, course_schema, courses_schema
from models.padawans import Padawans, padawan_schema, padawans_schema
from models.padawan_courses_xref import padawan_course_enrollment_table 
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object



@authenticate_return_auth
def add_course(auth_info):
  if auth_info.user.role =='admin':
    post_data = request.form if request.form else request.get_json()

    new_course = Courses.new_course_obj()
    populate_object(new_course, post_data)
    try:
      db.session.add(new_course)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to add course. {e}"}), 400
    
    return jsonify({"message": "course added", "result": course_schema.dump(new_course)}), 201
  return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth #Master+ rank required
def enroll_padawan(auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    post_data = request.form if request.form else request.get_json()

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == post_data['padawan_id']).first()
    course_query = db.session.query(Courses).filter(Courses.course_id == post_data['course_id']).first()

  if not padawan_query:
    return jsonify({"message":"unable to complete enrollment, padawan id not found"}), 404
  
  elif not course_query:
    return jsonify({"message":"unable to complete enrollment, course id not found"}), 404
  
  if padawan_query and course_query:
    padawan_query.courses.append(course_query)
    db.session.commit()

    return jsonify({"message": "padawan successfuly enrolled in course", "result": course_schema.dump(course_query)}), 201  
  return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth #anyone
def get_course(difficulty_level, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    course_query = db.session.query(Courses).filter(Courses.difficulty == difficulty_level).all()

    if not course_query:
      return jsonify({"message": "no courses found"}), 404

    return jsonify({"message": "courses retrieved", "results": courses_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #Instructor or Council+ required
def update_course(course_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    post_data = request.form if request.form else request.get_json()

    if not course_query:
      return jsonify({"message": "unable to update record"}), 400
    
    populate_object(course_query, post_data)

    db.session.commit()

    return jsonify({"message": "course updated", "results": course_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth #Instructor or Council+ required, handle enrollements
def delete_course(course_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not course_query:
      return jsonify({"message": f"no course found with id {course_id}"}), 404
    try:
      db.session.delete(course_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to delete record. {e}"}), 400
    return jsonify({"message": "course deleted", "result": course_schema.dump(course_query)}), 200
  return jsonify({"message": "unauthorized"}), 401

  
@authenticate_return_auth #anyone
def remove_padawan_enrollment(padawan_id, course_id, auth_info):
  if auth_info.user.role == 'admin' or auth_info.user.role == 'user':
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    if not padawan_query:
      return jsonify({"message":"unable to remove padawan from course, padawan id invalid"}), 404
    
    elif not course_query:
      return jsonify({"message":"unable to remove padawan from course, course id invalid"}), 404
    
    enrollment_query = db.session.query(padawan_course_enrollment_table).filter(padawan_course_enrollment_table.course_id == course_id and padawan_course_enrollment_table.padawan_id == padawan_id).first()

    if not enrollment_query:
      return jsonify({"message":"unable to remove padawan from course, padawan isn't enrolled."}), 404

    try:
      db.session.delete(enrollment_query)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      return jsonify({"message": f"unable to remove enrollment. {e}"}), 400
    return jsonify({"message": "enrollment removed", "result": course_schema.dump(course_query)}), 200

  return jsonify({"message": "unauthorized"}), 401