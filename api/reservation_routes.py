from flask import Blueprint, jsonify, request
from repositories.reservation_repository import db_get_reservations

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
    
    

    