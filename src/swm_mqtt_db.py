import mysql.connector
import json
import paho.mqtt.client as mqtt
from datetime import datetime
import argparse
import sys
import logging
from config import DB_CONFIG, MQTT_CONFIG

# Set up logging for error handling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MQTT Client for Waste Management Dashboard")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
verbose = args.verbose

# Function to create a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if verbose:
            logger.info("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to database: {err}")
        return None

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        if verbose:
            logger.info("Connected to MQTT Broker successfully!")
        client.subscribe(MQTT_CONFIG['topic'])
    else:
        logger.error(f"Failed to connect to MQTT Broker, return code: {rc}")

# MQTT on_message callback
def on_message(client, userdata, msg):
    try:
        # Parse the JSON payload
        data = json.loads(msg.payload)
        device_id = data['device_id']
        fullness_level = data['fullness_level']
        timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Print received message if verbose
        if verbose:
            logger.info(f"Received message: Device ID = {device_id}, Fullness Level = {fullness_level}, Timestamp = {timestamp}")

        # Insert data into MySQL database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO readings (device_id, timestamp, fullness_level) "
                "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE "
                "timestamp = VALUES(timestamp), fullness_level = VALUES(fullness_level)",
                (device_id, timestamp, fullness_level)
            )
            conn.commit()
            cursor.close()
            conn.close()
            if verbose:
                logger.info(f"Data inserted: Device ID = {device_id}, Fullness Level = {fullness_level}, Timestamp = {timestamp}")

            # Alert if fullness level is over 80%
            if fullness_level > 80:
                logger.warning(f"Alert: {device_id} is over 80% full!")
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON message from {msg.payload}")
    except mysql.connector.Error as db_err:
        logger.error(f"Database error: {db_err}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Set up the MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_CONFIG['username'], MQTT_CONFIG['password'])
client.tls_set()  # Use default CA certificates for TLS encryption
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
if verbose:
    logger.info("Connecting to MQTT broker...")
try:
    client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], 60)
except Exception as e:
    logger.error(f"Error connecting to MQTT broker: {e}")
    sys.exit(1)

# Start the MQTT loop
client.loop_forever()
