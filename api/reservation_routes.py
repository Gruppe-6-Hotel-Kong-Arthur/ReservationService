from flask import Blueprint, jsonify, request
import os, requests
from repositories.reservation_repository import (
    db_get_reservations, 
    db_get_reservation,
    db_make_reservation,
)

GUEST_SERVICE_URL = os.getenv('GUEST_SERVICE_URL')
ROOM_INVENTORY_SERVICE_URL = os.getenv('ROOM_INVENTORY_SERVICE_URL')

# Blueprint for reservation routes
reservation_routes = Blueprint('reservation_routes', __name__)

# GET all reservations
@reservation_routes.route('', methods=['GET'])
def get_reservations():
    try:
        reservations = db_get_reservations()
        return jsonify(reservations), 200 if reservations else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST a new reservation
@reservation_routes.route('/new', methods=['POST'])
def new_reservation():
    data = request.json()
    guest_id = data.get('guest_id')
    room_id = data.get('room_id')
    season_id = data.get('season_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not guest_id or not room_id or not season_id or not start_date or not end_date:
        return jsonify({"error": "Missing required fields"}), 400

    # make reservation
    db_make_reservation(guest_id, room_id, season_id, start_date, end_date)

# GET a reservation by id
@reservation_routes.route('/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    try:
        reservation = db_get_reservation(reservation_id)

        print(f'Reservation: {reservation}')

        # Make a request to the guest service to get guest 
        guest_response = requests.get(f'{GUEST_SERVICE_URL}/api/v1/guests/{reservation["guest_id"]}')
        guest_information = guest_response.json()

        print(f'Guest Information: {guest_information}')

        # Make a request to the room inventory service to get room information
        room_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/rooms/{reservation["room_id"]}')
        room_information = room_response.json()

        print(f'Room Information: {room_information}')

        response = {
            "reservation_id": reservation_id,
            "first_name": guest_information["first_name"],
            "last_name": guest_information["last_name"],
            "country": guest_information["country"],
            "room_id": reservation["room_id"],
            "room_type": room_information["type_name"],
            "price": reservation["price"]
        }

        print(f'Response: {response}')

        return jsonify(response), 200 if response else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500