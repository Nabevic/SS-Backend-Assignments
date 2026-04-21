from flask import Blueprint

import controllers


event = Blueprint('event', __name__)


@event.route('/event', methods=['POST'])
def add_event_route():
  return controllers.add_event()

@event.route('/events', methods=['GET'])
def get_all_events_route():
  return controllers.get_all_events()

@event.route('/event/<date>', methods=['GET'])
def get_event_by_date_route(date):
  return controllers.get_event_by_date(date)

@event.route('/event/<event_id>', methods=['GET', 'PUT'])
def event_by_id_route(event_id):
  return controllers.event_by_id(event_id)

@event.route('/event/delete', methods=['DELETE'])
def delete_event_route():
  return controllers.delete_event()