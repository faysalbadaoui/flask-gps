from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('gps_data')  # This is where your ESP32 should emit
def handle_gps_data(data):
    print("Received GPS:", data)
    # Broadcast the GPS update to all clients (like your dashboard)
    emit('gps_update', data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
