# backend/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)
latest_location = {'lat': 0.0, 'lon': 0.0}

@app.route('/gps', methods=['POST'])
def gps():
    global latest_location
    data = request.json
    latest_location['lat'] = data.get('latitude')
    latest_location['lon'] = data.get('longitude')
    return jsonify({'status': 'OK'})

@app.route('/location', methods=['GET'])
def location():
    return jsonify(latest_location)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
