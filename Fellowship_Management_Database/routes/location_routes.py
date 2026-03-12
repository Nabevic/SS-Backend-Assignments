from flask import Blueprint
import controllers


location = Blueprint('location', __name__)


@location.route("/location", methods=['POST'])
def add_location():
  return controllers.add_location()

@location.route("/location/<location_id>", methods=['GET','PUT'])
def location_by_id(location_id):
  return controllers.location_by_id(location_id)

@location.route("/location/delete/<location_id>", methods=['DELETE'])
def delete_location(location_id):
  return controllers.delete_location(location_id)