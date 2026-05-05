from flask import jsonify, request
from db import db
from models.events import Events, event_schema, events_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, auth_level



@authenticate_return_auth 
def add_event(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  post_data = request.form if request.form else request.json

  new_event = Events.new_event_obj()
  populate_object(new_event, post_data)

  try:
    db.session.add(new_event)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to add event. {e}"}), 400

  return jsonify({"message": "event created","result": event_schema.dump(new_event)}), 201



@authenticate_return_auth 
def get_all_events(auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  event_query = db.session.query(Events).all()

  if not event_query:
    return jsonify({"message": "no events found"}), 404

  return jsonify({"message": "events retrieved", "results": events_schema.dump(event_query)}), 200



@authenticate_return_auth 
def get_events_by_date(date, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  event_query = db.session.query(Events).filter(Events.date == date).all()

  if not event_query:
    return jsonify({"message": "no events found"}), 404

  return jsonify({"message": "events retrieved", "results": events_schema.dump(event_query)}), 200



@authenticate_return_auth 
def event_by_id(event_id, auth_info):
  if auth_info.user.role not in auth_level['user']:
    return jsonify({"message": "unauthorized"}), 401
  event_query = db.session.query(Events).filter(Events.event_id == event_id).first()
  if not event_query:
    return jsonify({"message": "no event found"}), 404

  if request.method == 'GET':
    return jsonify({"message": "event retrieved", "results": event_schema.dump(event_query)}), 200
  
  elif request.method == "PUT":
    if auth_info.user.user_id == event_query.host_id or auth_info.user.role in auth_level['admin']:
      put_data = request.form if request.form else request.get_json()
      populate_object(event_query, put_data)

      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"unable to update event. {e}"}), 400
      return jsonify({"message": "event updated", "results": event_schema.dump(event_query)}), 200
    return jsonify({"message": "unauthorized"}), 401
    


@authenticate_return_auth
def delete_event(auth_info):
  if auth_info.user.role not in auth_level['super']:
    return jsonify({"message": "unauthorized"}), 401
  request_data = request.form if request.form else request.json
  event_query = db.session.query(Events).filter(Events.event_id == request_data["event_id"]).first()
  if not event_query:
    return jsonify({"message": f"no event found with id {request_data['event_id']}"}), 400
  
  try:
    db.session.delete(event_query)
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to delete record. {e}"}), 400
  
  db.session.commit()
  return jsonify({"message": "event deleted", "result": event_schema.dump(event_query)}), 200