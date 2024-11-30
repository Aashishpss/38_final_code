# Vehicle-to-Vehicle (V2V) Communication System

This project simulates a vehicle-to-vehicle communication system using hardware (ESP8266/ESP32), a server, and a web-based dashboard. The system integrates real-world hardware with a simulation environment to showcase dynamic platooning and traffic management.

## Table of Contents
1. [Project Components](#project-components)
2. [Setup and Installation](#setup-and-installation)
   - [Client Setup](#client-setup)
   - [Server Setup](#server-setup)
3. [Usage](#usage)
4. [Hardware]
4. [File Structure](#file-structure)
5. [Contributing](#contributing)


## Project Components

### 1. Client Devices
Each client represents a vehicle equipped with specific sensors and capabilities:
- **Client 1**: Ultrasonic sensor and raindrop sensor.
- **Client 2**: Ultrasonic sensor and DHT22 sensor (temperature and humidity).
- **Client 3**: Ultrasonic sensor.

### 2. Server
- Receives real-time data from clients.
- Sends commands for vehicle control.
- Updates a MongoDB database with the latest data.

### 3. Dashboard
A Flask-based web application that:
- Fetches real-time data from MongoDB.
- Displays sensor data and vehicle states.

### 4. Simulation
Utilizes the SUMO simulator with TraCI integration to:
- Model vehicle platooning.
- Simulate urban road conditions with dynamic traffic.

## Setup and Installation

### Client Setup

#### Prerequisites
- **Hardware**: ESP8266/ESP32.
- Install the **Arduino IDE** and ESP8266/ESP32 board support.

#### Configuration
1. Update the **Wi-Fi SSID, password, and server IP address** in the client code.
2. Flash the appropriate code onto each ESP device:
   - **Client 1**: `Car1.cpp`
   - **Client 2**: `Car2.cpp`
   - **Client 3**: `Car3.cpp`

### Server Setup

#### Prerequisites
- Install Python 3.x.
- Install required Python libraries:
  ```bash
  pip install flask flask-socketio pymongo
- Set all path variables correctly

# Dashboard Setup
1; Navigate to the Dashboard directory
2; Run the Flask application:
   ```bash
   python app.py
   ```
3; Go to underlined link in the terminal to open the dashboard.

workflow for dashboard-
1. Server uploads data into the mongodb database.
2. dashboard fetches the data from mongodb and shows it onto the webpage.
3. The latency for fetching data is set at 1 ms.

Usage 
1; Start the server
2; Power on the client devices
3; Open the dashboard in a web browser to monitor real-time data and control the vehicles.

Final Results
![Login Page](Images/Dashboard_signup_page.png)
![Dashboard](Images/dynamic_dashboard.png)
![Contact Page](Images/contact_us.png)

# Simulation Setup
1; Ensure that SUMO is installed and added to the system PATH.
2; Run the SUMO simulation:
   ```bash
   sumo-gui -c "simulation files/tinker-final.sumocfg"
   ```

For this simulation, we used the SUMO simulator along with SUMO-GUI and Python (via TraCI). The road network was generated using the OSM Web Wizard, and routes and vehicles were defined using NetEdit. The entire simulation was controlled through a Python script that integrates TraCI with the SUMO configuration.

Simulation Details:

	•	Platoon 1: The leader is colored blue, with pink followers. Other traffic is represented in yellow.
	•	Platoon 2: The leader is brown, and the followers are purple. 

This platoon dynamically adjusts speeds to maintain a consistent gap. If the distance increases, the leader slows down, and the followers speed up to close the gap.

Despite encountering traffic lights and varying road conditions, both platoons maintain proper spacing and reach their destinations simultaneously, demonstrating coordinated platoon behavior.


# Circuit Diagram
The basic circuit diagram for the client devices is as follows:
![Circuit Diagram](Images/basic%20circuit.jpg)

For each car, some sensor may be connected. That connection mapping can be found in the respective code files.

## mapping for pins:
D0	GPIO16	No PWM support, used for Wakeup
D1	GPIO5	General-purpose I/O, PWM support
D2	GPIO4	General-purpose I/O, PWM support
D3	GPIO0	General-purpose I/O, often used for boot mode
D4	GPIO2	General-purpose I/O, often used for boot mode
D5	GPIO14	General-purpose I/O, PWM support
D6	GPIO12	General-purpose I/O, PWM support
D7	GPIO13	General-purpose I/O, PWM support
D8	GPIO15	General-purpose I/O, often used for boot mode
D9	GPIO3	RX pin, used for serial communication
D10	GPIO1	TX pin, used for serial communication
A0	Analog (A0)	ADC, reads analog values (0-1V)

## Hardware used:
3 Ultra sonic sensors
12 motor drivers and wheels
1 raindrop sendor
1 DHT22 sensor
3 ESP8266/ESP32 
Jumper wires
3 motor drivers

## Final Results
![Car1](Images/car1.jpg)
![Car2](Images/car2.jpg)
![Car3](Images/car3.jpg)


# File Structure
```
.
├── .gitignore
├── .vscode/
│   ├── c_cpp_properties.json
│   ├── launch.json
│   └── settings.json
├── 38_Adaptive Vehicle Platooning System_V2V Communication_G1/
│   └── 38_Adaptive Vehicle Platooning System_V2V Communication_G1.pptx
├── [Car1.cpp](http://_vscodecontentref_/0)
├── [Car2.cpp](http://_vscodecontentref_/1)
├── [Car3.cpp](http://_vscodecontentref_/2)
├── Dashboard/
│   ├── __pycache__/
│   ├── app.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   └── ...
├── [readme.md](http://_vscodecontentref_/3)
├── [server.py](http://_vscodecontentref_/4)
├── simulation files/
│   ├── final.py
│   ├── tinker-final.add.xml
│   ├── tinker-final.con.xml
│   ├── tinker-final.dat.xml
│   ├── tinker-final.edg.xml
│   ├── tinker-final.netecfg
│   ├── tinker-final.nod.xml
│   ├── tinker-final.rou.xml
│   ├── tinker-final.sumocfg
│   ├── tinker-final.typ.xml
│   └── ...
├── [sound.py](http://_vscodecontentref_/5)
└── [tempCodeRunnerFile.py](http://_vscodecontentref_/6)
```

# Contributers :
1; Aashish Singh
2; Lakshay Kumar
3; Shivam Goyal
4; Arun
5; Arpit

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
