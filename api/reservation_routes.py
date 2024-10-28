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

# GET all reservations with guest and room details
@reservation_routes.route('', methods=['GET'])
def get_reservations():
    try:
        reservations = db_get_reservations()

        # Construct response object with guest, room, and reservation details
        response_list = []
        for reservation in reservations:
            # Make a request to the guest service to get guest information
            guest_response = requests.get(f'{GUEST_SERVICE_URL}/api/v1/guests/{reservation["guest_id"]}')
            guest_information = guest_response.json()
            
            # Make a request to the room inventory service to get room information
            room_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/rooms/{reservation["room_id"]}')
            room_information = room_response.json()
            
            # Construct response object and append to response list
            response = _format_reservation_response(reservation, guest_information, room_information)
            response_list.append(response)

        return jsonify(response_list), 200 if response_list else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET a reservation by id with guest and room details
@reservation_routes.route('/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    try:
        reservation = db_get_reservation(reservation_id)

        # Make a request to the guest service to get guest 
        guest_response = requests.get(f'{GUEST_SERVICE_URL}/api/v1/guests/{reservation["guest_id"]}')
        guest_information = guest_response.json()

        # Make a request to the room inventory service to get room information
        room_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/rooms/{reservation["room_id"]}')
        room_information = room_response.json()

        # Construct response object with reservation, guest, and room information
        response = _format_reservation_response(reservation, guest_information, room_information)

        return jsonify(response), 200 if response else 404
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


# ------------------------------ Helper Functions ------------------------------ #

# Helper function to format reservation response
def _format_reservation_response(reservation, guest_info, room_info):
    return {
        "reservation_id": reservation["id"],
        "guest": {
            "guest_id": guest_info.get("id"),
            "first_name": guest_info.get("first_name"),
            "last_name": guest_info.get("last_name"),
            "country": guest_info.get("country"),
        },
        "room": {
            "room_id": room_info.get("id"),
            "room_type": room_info.get("type_name"),
        },
        "reservation_details": {
            "start_date": reservation.get("start_date"),
            "end_date": reservation.get("end_date"),
            "price": reservation.get("price"),
            "days_rented": int(reservation.get("days_rented")), # Convert to integer
        }
    }