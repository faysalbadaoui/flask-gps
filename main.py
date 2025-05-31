from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

def write_gps_to_file(lat, lon):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("gps_log.txt", "a") as f:
        f.write(f"{timestamp} - Latitude: {lat}, Longitude: {lon}\n")

def read_gps_from_file():
    try:
        with open("gps_log.txt", "r") as f:
            lines = f.readlines()
        coordinates = []
        for line in lines:
            # Parse each line into timestamp and coordinates
            parts = line.strip().split(" - ")
            if len(parts) == 2:
                timestamp, coords = parts
                lat_lon = coords.replace("Latitude: ", "").replace("Longitude: ", "").split(", ")
                coordinates.append({
                    "timestamp": timestamp,
                    "latitude": float(lat_lon[0]),
                    "longitude": float(lat_lon[1])
                })
        return coordinates
    except FileNotFoundError:
        return []

@app.route('/gps', methods=['POST'])
def receive_gps():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # Handle alert payload
    if "alert" in data:
        alert_msg = data["alert"]
        print(f"🔔 ALERT from device: {alert_msg}")
        return jsonify({"status": "alert received"}), 200

    # Handle normal GPS payload
    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is None or lon is None:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    print(f"Received GPS data → Latitude: {lat}, Longitude: {lon}")
    write_gps_to_file(lat, lon)
    return jsonify({"status": "gps received"}), 200

@app.route('/gps', methods=['GET'])
def get_gps():
    coordinates = read_gps_from_file()
    return jsonify({
        "count": len(coordinates),
        "coordinates": coordinates
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
