from flask import Flask, request, jsonify
from calendly_api.services.availability_service import AvailabilityService

app = Flask(__name__)
service = AvailabilityService()

@app.route('/initialize_user', methods=['POST'])
def initialize_user():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    service.initialize_user(user_id)
    return jsonify({"message": f"User {user_id} initialized successfully"}), 201

@app.route('/set_availability', methods=['POST'])
def set_availability():
    user_id = request.json.get('user_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    available = request.json.get('available')
    if not user_id or not start_time or not end_time or available is None:
        return jsonify({"error": "user_id, start_time, end_time, and available are required"}), 400
    try:
        service.set_availability(user_id, start_time, end_time, available)
        return jsonify({"message": f"Availability for {user_id} updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update_availability', methods=['POST'])
def update_availability():
    user_id = request.json.get('user_id')
    updates = request.json.get('updates')
    if not user_id or not updates:
        return jsonify({"error": "user_id and updates are required"}), 400
    try:
        service.update_availability(user_id, updates)
        return jsonify({"message": f"Availability for {user_id} updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/is_available', methods=['GET'])
def is_available():
    user_id = request.args.get('user_id')
    time = request.args.get('time')
    if not user_id or not time:
        return jsonify({"error": "user_id and time are required"}), 400
    try:
        availability = service.is_available(user_id, time)
        return jsonify({"available": availability}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/find_availability', methods=['GET'])
def find_availability():
    user_id = request.args.get('user_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    if not user_id or not start_time or not end_time:
        return jsonify({"error": "user_id, start_time, and end_time are required"}), 400
    try:
        available_slots = service.find_availability(user_id, start_time, end_time)
        return jsonify({"available_slots": available_slots}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/find_overlap', methods=['GET'])
def find_overlap():
    user1_id = request.args.get('user1_id')
    user2_id = request.args.get('user2_id')
    if not user1_id or not user2_id:
        return jsonify({"error": "user1_id and user2_id are required"}), 400
    try:
        overlaps = service.find_overlap(user1_id, user2_id)
        return jsonify({"overlapping_slots": overlaps}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
