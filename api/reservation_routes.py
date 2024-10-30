from flask import Blueprint, jsonify, request
import os, requests
from datetime import datetime
from repositories.reservation_repository import (
    db_get_reservations, 
    db_get_reservation,
    db_make_reservation,
)

GUEST_SERVICE_URL = os.getenv('GUEST_SERVICE_URL')
ROOM_INVENTORY_SERVICE_URL = os.getenv('ROOM_INVENTORY_SERVICE_URL')

# Blueprint for reservation routes
reservation_routes = Blueprint('reservations', __name__)

# GET all reservations with guest and room details
@reservation_routes.route('', methods=['GET'])
def get_reservations():
    try:
        reservations = db_get_reservations()
        
        # Get guest and room details for each reservation with helper function and list comprehension
        response_list = [ _get_reservation_with_details(reservation) for reservation in reservations ]

        return jsonify(response_list), 200 if response_list else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET a reservation by id with guest and room details
@reservation_routes.route('/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    try:
        reservation = db_get_reservation(reservation_id)
        response = _get_reservation_with_details(reservation)
        return jsonify(response), 200 if response else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST a new reservation
@reservation_routes.route('/new', methods=['POST'])
def new_reservation():
    try:
        data = request.get_json()
        guest_id = data.get('guest_id')
        room_id = data.get('room_id')
        start_date = data.get('start_date')  # Keep as string
        end_date = data.get('end_date')      # Keep as string

        # Check for required fields
        if not guest_id or not room_id or not start_date or not end_date:
            return jsonify({"error": "Missing required field(s)"}), 400

        # Get room information from room inventory service
        room_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/rooms/{room_id}')
        room_information = room_response.json()
        print(f'Room Information: {room_information}')

        if 'error' in room_information:
            return jsonify({"error": f"Room retrieval error: {room_information['error']}"}), 404

        # Get season information from room inventory service
        season_response = requests.get(
            f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/calculate_price/{room_information["room_type_id"]}?start_date={start_date}&end_date={end_date}'
        )
        season_information = season_response.json()
        print(f'Season Information: {season_information}')

        # Check if season information is valid and contains the required ID
        if 'season' not in season_information or 'id' not in season_information['season']:
            return jsonify({"error": "Season information does not contain an ID."}), 400

        # Use the correct ID from the nested structure
        season_id = season_information['season']['id']

        db_make_reservation(guest_id, room_id, season_id, start_date, end_date, season_information["price"])
        return jsonify({"message": "Reservation created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------ Helper Functions ------------------------------ #

# Helper function to get guest and room details for all reservations
def _get_reservation_with_details(reservation):
    try:
        if not reservation:
            raise Exception("Reservation not found")

        # Get guest information from guest service
        guest_response = requests.get(f'{GUEST_SERVICE_URL}/api/v1/guests/{reservation["guest_id"]}')
        guest_information = guest_response.json()
        
        # Get room information from room inventory service
        room_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/rooms/{reservation["room_id"]}')
        room_information = room_response.json()

        # Get room information from room inventory service
        season_response = requests.get(f'{ROOM_INVENTORY_SERVICE_URL}/api/v1/calculate_price/season_type/{reservation["season_id"]}')
        season_informatino = season_response.json()
        
        return _format_reservation_response(
            reservation, 
            guest_information, 
            room_information,
            season_informatino
        )
    except Exception as e:
        return {"error": str(e)}

# Helper function to format reservation response
def _format_reservation_response(reservation, guest_information, room_information, season_informatino):
    try:
        if not guest_information or not room_information or not season_informatino:
            raise Exception("Guest or room or season type not found")
        
        return {
        "reservation_id": reservation["id"],
        "guest": {
            "guest_id": guest_information.get("id"),
            "first_name": guest_information.get("first_name"),
            "last_name": guest_information.get("last_name"),
            "country": guest_information.get("country"),
        },
        "room": {
            "room_id": room_information.get("id"),
            "room_type": room_information.get("type_name"),
        },
        "reservation_details": {
            "start_date": reservation.get("start_date"),
            "end_date": reservation.get("end_date"),
            "price": reservation.get("price"),
            "days_rented": int(reservation.get("days_rented")), # Convert to integer
            "season": season_informatino.get("season_type")
        }
    }
    except Exception as e:
        return {"error": str(e)}