from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room, send
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Sample specialists data (replace with database integration)
specialists = [
    {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "location": {"lat": 34.0522, "lng": -118.2437}},
    {"id": 2, "name": "Dr. Brown", "specialization": "Neurologist", "location": {"lat": 40.7128, "lng": -74.0060}},
    {"id": 3, "name": "Dr. Taylor", "specialization": "Dermatologist", "location": {"lat": 37.7749, "lng": -122.4194}},
]

# Route for the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to find nearby specialists
@app.route('/find_specialists', methods=['POST'])
def find_specialists():
    user_location = request.json.get('location')
    # Logic to filter specialists based on location
    nearby_specialists = specialists  # Replace with actual filtering logic
    return jsonify(specialists=nearby_specialists)

# SocketIO event handlers for chat
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    send(f"{data['username']} has joined the room.", to=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} has left the room.", to=room)

@socketio.on('message')
def handle_message(data):
    send(data['msg'], to=data['room'])

# SocketIO event handler for video signals
@socketio.on('signal')
def on_signal(data):
    room = data['room']
    signal_data = data['signalData']
    socketio.emit('signal', {'signalData': signal_data}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
