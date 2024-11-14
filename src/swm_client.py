import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime
from config import MQTT_CONFIG, COMPACTORS, UPDATE_INTERVAL  # Import from the config file

def generate_reading(compactor):
    # Gradually increase the fullness level (ensure it doesn't decrease)
    # Increment the fullness level by a random value between 1 and 5
    increment = random.randint(1, 5)
    compactor["fullness_level"] = min(compactor["fullness_level"] + increment, 100)  # Cap the fullness at 100%

    timestamp = datetime.utcnow().isoformat()  # Use UTC timestamp
    # Create the payload to send in the MQTT message
    payload = {
        "device_id": compactor["device_id"],
        "fullness_level": compactor["fullness_level"],
        "timestamp": timestamp
    }
    return json.dumps(payload)

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        for compactor in COMPACTORS:
            # Subscribe to each device's topic (if necessary)
            # Here we're just sending data, so no subscribe needed
            print(f"Ready to send data for {compactor['device_id']}")
    else:
        print("Failed to connect, return code: " + str(rc))

# MQTT on_publish callback
def on_publish(client, userdata, mid):
    print(f"Message Published! Mid: {mid}")

# Set up the MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_CONFIG['username'], MQTT_CONFIG['password'])  # Set MQTT credentials
client.tls_set()  # Use default CA certificates for TLS encryption
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker using the configuration from config.py
client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], 60)

# Start the MQTT loop to maintain connection
client.loop_start()

# Simulate the devices sending data every 10 seconds
while True:
    for compactor in COMPACTORS:
        # Generate a random fullness level reading for the current device
        reading = generate_reading(compactor)
        # Publish the message to the MQTT broker
        client.publish(MQTT_CONFIG['topic'], reading)
        print(f"Sent data for {compactor['device_id']} to MQTT broker: {reading}")
    time.sleep(UPDATE_INTERVAL)  # Wait for 10 seconds before sending again