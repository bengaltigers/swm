# Smart Waste Management - Architecture

## Introduction
The Software Waste Management (SWM) system provides an intelligent, end-to-end solution for tracking and managing waste compactor fullness levels across urban and regional zones. Using MQTT as the core communication protocol, the system ensures reliable data transfer between IoT devices and backend servers. Each waste compactor device sends periodic fullness updates to a central MQTT broker, where an MQTT handler processes the data and stores it in a MySQL database, enabling real-time data availability.

For users, the SWM dashboard displays the latest data from all compactors, providing insights such as average daily fullness levels and potential high-usage patterns. Additional features include route mapping for optimized waste collection and an admin console for system management. The management console allows administrators to monitor device statuses, manage zone configurations, set alert thresholds, and perform user management tasks, providing a comprehensive solution for efficient waste management across multiple zones.

![image](https://github.com/user-attachments/assets/d157a3d7-343d-48a8-848c-52b31232c36b)


### 1. **BIN Software**

- **Purpose**: Each BIN device (acting as an IoT device) simulates or measures the waste compactor’s fullness level, sending data to the MQTT broker.
- **Key Functions**: Sensor data acquisition, connection to MQTT broker, publishing of waste data, and sending periodic updates.
- **Data Format**: JSON messages with fields such as `device_id`, `fullness_level`, and `timestamp` are sent to ensure consistency in data processing across different modules.
- **Deployment Flexibility**: Supports various geographic locations and devices with different configurations, making it adaptable for a wide range of urban waste management needs.

  ![image](https://github.com/user-attachments/assets/eee1ad78-4fd2-4cd9-aa17-42aeb54088fb)


### 2. **MQTT & DB Handlers with Alert System**

- **Purpose**: Acts as the intermediate data processing unit between the BIN software and the backend. This handler subscribes to the MQTT topic, parses the BIN data, stores it in the database, and triggers alerts based on predefined thresholds.
- **Key Functions**:
  - **Database Insertion**: Uses MySQL to store `device_id`, `fullness_level`, and timestamp in a relational format for efficient querying.
  - **Data Validation**: Filters duplicate or erroneous data entries and only keeps the most recent reading.
  - **Alert Mechanism**: Sends alerts when fullness levels exceed a specified threshold (e.g., 80%), allowing for timely waste collection.
- **Scalability**: Multiple instances can be deployed for citywide or regional zones. For example, each zone can have its own handler instance to manage data flow independently.
- **Reliability**: Automatic reconnect and error-handling mechanisms in case of MQTT or database connection issues.

- ![image](https://github.com/user-attachments/assets/c7555a22-804e-4a5a-84fd-a0d12f9e0544)


### 3. **Backend Server (Dashboard and System Management)**

- **Purpose**: Provides a user-friendly web dashboard for real-time monitoring and historical analysis of waste compactors.
- **Key Functions**:
  - **Data Visualization**: Presents fullness levels, alerts, and status updates for all compactors.
  - **Average Daily Fullness**: Calculates and displays daily average fullness levels for trend analysis.
  - **Device Management**: Allows system administrators to add/remove devices, define zones, and set alert thresholds.
- **Component Organization**: Each backend instance is responsible for one or more zones and can be configured to scale horizontally as demand grows.

- ![image](https://github.com/user-attachments/assets/2e2f1b3c-9677-4db6-ac38-b2af62e54d65)


### Future Considerations

- **Client Management**: Integrate user accounts, user roles, and permission levels to improve system security and allow for multi-user access.
- **Route Optimization**: Machine learning algorithms could optimize waste collection routes based on real-time data to reduce costs.
- **Usage Pattern Analytics**: Leverage predictive analytics and AI to identify patterns in waste collection, enabling proactive resource allocation in high-demand areas.
- **Enhanced Alerting**: Configurable alerts (via SMS, email) with thresholds based on historical patterns and dynamic thresholds for peak usage periods.

