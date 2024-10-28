from flask import Flask, jsonify
from api.reservation_routes import reservation_routes
from database.initialization import init_db

app = Flask(__name__)

# Register blueprints for modular endpoints
app.register_blueprint(reservation_routes, url_prefix='/api/v1/reservations')

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Initializes database and runs Flask app on port 5003
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5003, debug=True)