from flask import Flask, jsonify
import mysql.connector
import json
#from datetime import datetime
import sys
from dashboard import init_dashboard  # Import the function to initialize Dash app
from config import DB_CONFIG

app = Flask(__name__)

# Initialize Flask app
app = Flask(__name__)

# Create MySQL connection function
def get_db_connection():
    print('This is error output db', file=sys.stderr)
    print('This is standard output db', file=sys.stdout)
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


@app.route('/')
def index():
    print('This is error output t', file=sys.stderr)
    print('This is standard output t', file=sys.stdout)
    return "BT SWM System with MQTT & Python"

# Endpoint to list all devices
@app.route('/devices', methods=['GET'])
def list_devices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices;")
    devices = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(devices)

# Endpoint to get readings for a specific device
@app.route('/devices/<device_id>/readings', methods=['GET'])
def get_readings(device_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readings WHERE device_id = %s;", (device_id,))
    readings = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(readings)


# Initialize Dash app on the same Flask server
init_dashboard(app)  # Call function to set up Dash

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
