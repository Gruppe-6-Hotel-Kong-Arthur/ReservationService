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
        return jsonify({"message": "Reservation made successfully"}), 201
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
        
        return _format_reservation_response(
            reservation, 
            guest_information, 
            room_information
        )
    except Exception as e:
        return {"error": str(e)}

# Helper function to format reservation response
def _format_reservation_response(reservation, guest_info, room_info):
    try:
        if not guest_info or not room_info:
            raise Exception("Guest or room information not found")
        
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
    except Exception as e:
        return {"error": str(e)}