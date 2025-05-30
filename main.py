from flask import Flask, request, jsonify

app = Flask(__name__)

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
    return jsonify({"status": "gps received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
