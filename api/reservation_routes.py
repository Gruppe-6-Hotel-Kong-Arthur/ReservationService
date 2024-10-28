from flask import Blueprint, jsonify, request
# from repositories

# Blueprint for room routes
room_routes = Blueprint('reservations', __name__)

# GET all reservations
@room_routes.route('', methods=['GET'])
def get_reservations():
    pass
