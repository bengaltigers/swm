
# Waste Management Dashboard

## Introduction

This project implements a **Smart Waste Management (SWM) Dashboard** that integrates **MQTT**, **Flask**, and **Dash** to display real-time data on fullness levels of compactors. The system connects to a MySQL database to store the data and provides an interactive dashboard for viewing the collected data.

This project consists of three application components:

1. **Bin (IoT) Device Simulator**: A simulated IoT bin device that sends fullness levels as MQTT messages to a broker (hivemq.cloud).
2. **MQTT Subscriber & Database Storing Application**: A Python application that subscribes to incoming MQTT messages (`waste_management/readings`) from the bin devices and stores the data in a MySQL database.
3. **Backend Dashboard**: A Flask web application that serves as the backend for a data visualization dashboard, displaying the collected data.

---

## Prerequisites

Before running the application, ensure the following are installed:

1. Python 3.7 or later
2. MySQL database
3. MQTT broker for data publishing

---

## Installation

To get started with the project, clone the repository and install the dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/bengaltigers/swm.git
cd src
````

### Step 2: Install the required libraries

Create a virtual environment and install all the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Set up your MySQL Database

Make sure you have a MySQL database running and set up the required tables (`devices` and `readings`). Update the database connection configuration in the `dashboard.py` file with your MySQL credentials.
SWM project needs two tables in your MySQL database: devices and readings.

Table 1: devices
The devices table contains the registered devices with their unique device_id.

Schema:
```sql
CREATE TABLE devices (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL
);
```
- **device_id** (VARCHAR(50)): A unique identifier for the device.
- **device_name** (VARCHAR(100)): The name of the device.
- **location** (VARCHAR(255)): The location of the device.

**Table 2:** readings
The readings table stores the fullness levels sent by each device.

Schema:
```sql
CREATE TABLE readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fullness_level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (device_id),
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
```
- **reading_id** (INT AUTO_INCREMENT): A unique identifier for each reading.
- **device_id** (VARCHAR(50)): The identifier for the device. It must exist in the devices table before inserting data into readings.
- **timestamp** (TIMESTAMP): The time when the fullness level was recorded.
- **fullness_level** (INT): The fullness level of the device (0-100%).
- **created_at** (TIMESTAMP): The time when the reading was stored in the database.

**Note:** The device_id in the readings table must reference an existing device_id in the devices table. Make sure that the device is registered in the devices table before inserting readings.

---

## Usage

### Running the Projects

1. BIN Simulator

```bash
python swm_clinet.py
```

2. MQTT msg receiver & Storing inside database

```bash
python swm_mqtt_db.py
```

You can run the Flask app and the Dash dashboard by executing the following or from flask web framework (example PythonAnywhere):

```bash
python app.py
```

This will start both the Flask API and the Dash dashboard on `http://localhost:5000`.

1. The Flask app will serve the REST API for fetching device data and readings.
2. The Dash dashboard will display the data in a user-friendly table, which is automatically updated by clicking the "Refresh Data" button.

### Accessing the Dashboard

You can access the dashboard at:

- **Dashboard**: `http://localhost:5000/dashboard/`
- **Devices API**: `http://localhost:5000/devices/`
- **Device Readings API**: `http://localhost:5000/devices/<device_id>/readings`

---

## Project Structure

```
swm/
│
├── src/app.py               # Main Flask app
├── src/dashboard.py         # Dash dashboard app
├── src/swm_client.py        # BIN IOT simulator
├── src/swm_mqtt_db.py       # MQTT msg receiver & storage
├── src/config.py            # config files for DB & MQTT server access info
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── assets/                  # Optional folder for CSS, JS, images, etc.
└── config/                  # Optional configuration files
```

---

## Features

- **MQTT Integration**: Receives real-time data on fullness levels from MQTT broker.
- **Flask API**: Provides APIs to interact with the data stored in MySQL.
- **Dash Dashboard**: Displays the collected data in an interactive table with a refresh button.
- **MySQL Integration**: Stores data on device readings, including timestamps and fullness levels.

---

## Customization

You can modify the following components to fit your needs:

1. **MySQL Database Configuration**: Update the `db_config` dictionary with your own database credentials.
2. **MQTT Configuration**: Modify the MQTT broker settings (e.g., `MQTT_BROKER`, `MQTT_USERNAME`, etc.) to match your MQTT broker details.
3. **Dashboard**: Customize the Dash layout and add new components if necessary.

---

## ScreenShot

BIN Client
![cmd_dGnGwsKn8F](https://github.com/user-attachments/assets/fd3319b3-c060-4137-abe6-25f2df595a8c)

MQTT & DB hanlers
![image](https://github.com/user-attachments/assets/10d5ea93-a9c5-44c6-916f-d4ab247a1671)


Dashboard
![image](https://github.com/user-attachments/assets/8393b3c3-f97b-4138-ac13-cb692f74ee74)

Flask webserver @ pythonAnywhere
![image](https://github.com/user-attachments/assets/9be78358-759e-4d7c-9b7e-c9caeeaf789b)



## Troubleshooting

### Error: MQTT connection not established

- Ensure that the MQTT broker details are correctly configured and accessible from your machine.
- Check for any network issues or firewall restrictions preventing the connection.

### Error: MySQL connection fails

- Verify that the MySQL credentials and database details are correct.
- Ensure that the MySQL server is running and accessible.

---

## License

MIT License - See `LICENSE` file for details.

```

### How to copy:
1. Just copy everything from the start (`# Waste Management Dashboard`) to the end (`## License`).
2. Paste it directly into your `README.md` file.

This will allow you to copy everything in one go without any issues.

```

