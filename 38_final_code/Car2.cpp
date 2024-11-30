#include <ESP8266WiFi.h>
#include <DHT.h>

// Wi-Fi credentials
const char *ssid = "Arpit";        // Replace with your Wi-Fi SSID
const char *password = "12345678"; // Replace with your Wi-Fi password

// Server IP and port
const char *serverIP = "172.26.15.30"; // Replace with the laptop's server IP
const uint16_t serverPort = 12345;      // The same port as the server

// Ultrasonic sensor pins
#define TRIG_PIN 14 // GPIO14
#define ECHO_PIN 12 // GPIO12

// DHT sensor pin and type
#define DHT_PIN 2 // GPIO2
#define DHT_TYPE DHT22

// Motor driver pins
#define IN1 5  // GPIO5
#define IN2 4  // GPIO4
#define IN3 16 // GPIO16
#define IN4 0  // GPIO0
#define EN1 15 // GPIO15
#define EN2 13 // GPIO13

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient client;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Try to connect to the server
  while (!client.connect(serverIP, serverPort)) {
    Serial.println("Failed to connect to server, retrying...");
    delay(1000);
  }
  Serial.println("Connected to server");

  // Initialize ultrasonic sensor pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Initialize motor driver pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);

  // Enable motors
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  // Initialize DHT sensor
  dht.begin();
}

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2; // Convert to distance in cm
}

void stopCar() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  Serial.println("Car stopped.");
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Car moving forward.");
}

void overtakeObstacle() {
  // Rotate right
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(1000); // Adjust delay for semicircle rotation

  // Move forward
  moveForward();
  delay(2000); // Adjust delay for overtaking

  // Rotate left to original direction
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(1000); // Adjust delay for semicircle rotation

  // Move forward
  moveForward();
}

void setSpeed(bool halfSpeed) {
  if (halfSpeed) {
    analogWrite(EN1, 128); // Set speed to half
    analogWrite(EN2, 128); // Set speed to half
  } else {
    analogWrite(EN1, 255); // Set speed to full
    analogWrite(EN2, 255); // Set speed to full
  }
}

void loop() {
  // Check if the client is connected to the server
  if (!client.connected()) {
    Serial.println("Disconnected from server, attempting to reconnect...");
    while (!client.connect(serverIP, serverPort)) {
      Serial.println("Failed to connect to server, retrying...");
      delay(1000);
    }
    Serial.println("Reconnected to server");
  }

  // Get distance from the ultrasonic sensor
  long distance = getDistance();
  
  // Get temperature and humidity from the DHT sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Send the distance, temperature, and humidity to the server
  String data = "Distance: " + String(distance) + " cm, Temperature: " + String(temperature) + " C, Humidity: " + String(humidity) + " %\n";
  client.print(data);
  
  // Print the data on the Serial Monitor
  Serial.println(data);

  // Check for commands from the server
  if (client.available()) {
    String command = client.readStringUntil('\n');
    if (command == "STOP") {
      Serial.println("Received STOP command from server.");
      stopCar();
    } else if (command == "HELLO") {
      Serial.println("Received HELLO from server.");
    } else if (command == "OVERTAKE") {
      Serial.println("Received OVERTAKE command from server.");
      overtakeObstacle();
    } else if (command == "HALF_SPEED") {
      Serial.println("Received HALF_SPEED command from server.");
      setSpeed(true);
    } else if (command == "FULL_SPEED") {
      Serial.println("Received FULL_SPEED command from server.");
      setSpeed(false);
    }
  } else {
    moveForward();
  }

  // Wait for 1 second before sending the next data
  delay(1000);
}