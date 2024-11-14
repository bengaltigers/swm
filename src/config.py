# config.py

# Database Configuration
DB_CONFIG = {
    'host': 'bengaltiger.mysql.pythonanywhere-services.com',
    'user': 'bengaltiger',
    'password': 'xxxx',  # Replace with your actual password
    'database': 'bengaltiger$swm_dev0',  # Replace with your actual database name
}

# MQTT Broker Configuration
MQTT_CONFIG = {
    'broker': "3eb07ecaf65c4140a59c04f0aceabdf8.s1.eu.hivemq.cloud",  # MQTT broker URL
    'port': 8883,  # TLS/SSL port
    'topic': "waste_management/readings",  # Topic for waste management data
    'username': "mywms",  # MQTT username
    'password': "XXXX"  # MQTT password
}

# Simulated IoT devices (with fullness level)
COMPACTORS = [
    {"device_id": "compactor_1", "location": {"lat": 40.7128, "long": -74.0060}, "fullness_level": 0},
    {"device_id": "compactor_2", "location": {"lat": 34.0522, "long": -118.2437}, "fullness_level": 0}
]

# Simulated IoT fullness update interval
UPDATE_INTERVAL = 10
