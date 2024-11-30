import socket
import threading
import time
from pymongo import MongoClient
import pygame

def play_sound(file):
    #correct file path
    file= "sounds/"+file
    
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load(file)

    # Play the mp3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# MongoDB setup
client = MongoClient(
    "mongodb+srv://lakshu1000:lakshay1920@mlprojects.n13dkun.mongodb.net/&ssl=true&ssl_cert_reqs=CERT_NONE"
)
db = client["V2V"]
database = db["data"]

def updateWeather(id, val):
    filter = {'_id': 'weather'}
    update = {
        '$set': {
            f'val.{id}': f'{val}'
        }
    }
    database.update_one(filter, update)
    
def updateCars(id, distance, flag = 0):
    filter = {'_id': 'cars'}
    updateD = {
        '$set': {
            f'distance.{id}': f'{distance}'
        }
    }
    updateS = {
        '$set': {
            f'flag.{id}': f'{flag}'
        }
    }
    database.update_one(filter, updateD)
    database.update_one(filter, updateS)


# Server settings
server_ip = '0.0.0.0'
server_port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the IP and port
server_socket.bind((server_ip, server_port))

# Start listening for incoming connections (maximum 3 clients)
server_socket.listen(3)

print(f"Server is listening on {server_ip}:{server_port}")

# Accept connections from three clients
clients = []

for i in range(3):
    print(f"Waiting for client {i+1} to connect...")
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Client {i+1} connected: {client_address}")

# Function to handle client reconnection
def handle_client_reconnection(client_index):
    print(f"Waiting for client {client_index + 1} to reconnect...")
    client_socket, client_address = server_socket.accept()
    clients[client_index] = client_socket
    print(f"Client {client_index + 1} reconnected: {client_address}")

# Function to send "HELLO" message to all clients every 10 seconds
def send_hello_to_clients():
    while True:
        time.sleep(10)
        for client in clients:
            try:
                client.sendall("HELLO\n".encode('utf-8'))
                print("Sent HELLO to all clients")
            except Exception as e:
                print(f"Error sending HELLO to a client: {e}")

# Start the thread to send "HELLO" messages
hello_thread = threading.Thread(target=send_hello_to_clients)
hello_thread.daemon = True
hello_thread.start()

# Function to send command to all clients
def send_command_to_all_clients(command):
    for client in clients:
        try:
            client.sendall(f"{command}\n".encode('utf-8'))
        except Exception as e:
            print(f"Error sending {command} to a client: {e}")

# Receive and display data from the clients
while True:
    for i, client in enumerate(clients):
        try:
            data = client.recv(1024).decode('utf-8')
            if data:
                print(f"Received data from Client {i+1}: {data}")
                # Check if the distance is less than 5 cm
                if "Distance:" in data:
                    distance = float(data.split("Distance:")[1].strip().split()[0])
                    if distance < 10:
                        updateCars(i, distance, 1)
                        print(f"Distance from Client {i+1} is less than 5 cm. Sending STOP command to all clients.")
                        play_sound("Stop.mp3")
                        send_command_to_all_clients("STOP")
                        time.sleep(3)
                    elif 10 <= distance <= 20:
                        print(f"Distance from Client {i+1} is between 5 and 15 cm. Sending OVERTAKE command to all clients.")
                        send_command_to_all_clients("OVERTAKE")
                    updateCars(i, distance)
                    # Check if the distance from Client 2 is greater than 50 cm
                    if i == 1 and distance > 50:
                        print(f"Distance from Client 2 is greater than 50 cm. Sending HALF_SPEED command to Client 1.")
                        play_sound("Slow.mp3")
                        clients[0].sendall("HALF_SPEED\n".encode('utf-8'))
                    elif i == 1 and distance <= 50:
                        print(f"Distance from Client 2 is less than or equal to 50 cm. Sending FULL_SPEED command to Client 1.")
                        clients[0].sendall("FULL_SPEED\n".encode('utf-8'))
                    # Check if the distance from Client 3 is greater than 50 cm
                    if i == 2 and distance > 50:
                        print(f"Distance from Client 3 is greater than 50 cm. Sending HALF_SPEED command to Clients 1 and 2.")
                        play_sound("Slow.mp3")
                        clients[0].sendall("HALF_SPEED\n".encode('utf-8'))
                        clients[1].sendall("HALF_SPEED\n".encode('utf-8'))
                    elif i == 2 and distance <= 50:
                        print(f"Distance from Client 3 is less than or equal to 50 cm. Sending FULL_SPEED command to Clients 1 and 2.")
                        clients[0].sendall("FULL_SPEED\n".encode('utf-8'))
                        clients[1].sendall("FULL_SPEED\n".encode('utf-8'))
                    
                # Check if the temperature is greater than 30°C
                if "Temperature:" in data:
                    temperature = float(data.split("Temperature:")[1].strip().split()[0])
                    updateWeather('1', temperature)
                    if temperature > 30:
                        play_sound("DHT.mp3")
                        print(f"Temperature from Client {i+1} is greater than 30°C. Sending HALF_SPEED command to all clients.")
                        send_command_to_all_clients("HALF_SPEED")
                # Check if the humidity is greater than or equal to 97%
                if "Humidity:" in data:
                    humidity = float(data.split("Humidity:")[1].strip().split()[0])
                    updateWeather('0', humidity)
                    if humidity >= 97:
                        play_sound("DHT.mp3")
                        print(f"Humidity from Client {i+1} is greater than or equal to 97%. Sending HALF_SPEED command to all clients.")
                        send_command_to_all_clients("HALF_SPEED")
                # Check if the raindrop sensor value is less than 600
                if "Rain Level:" in data:
                    rain_level = int(data.split("Rain Level:")[1].strip().split()[0])
                    updateWeather('2', rain_level)
                    if rain_level < 600:
                        play_sound("Rain.mp3")
                        print(f"Rain Level from Client {i+1} is less than 600. Sending HALF_SPEED command to all clients.")
                        send_command_to_all_clients("HALF_SPEED")
            else:
                # Client disconnected
                print(f"Client {i+1} disconnected")
                clients[i].close()
                handle_client_reconnection(i)
        except Exception as e:
            # Handle any exceptions and try to reconnect the client
            print(f"Error with Client {i+1}: {e}. Attempting to reconnect...")
            clients[i].close()
            handle_client_reconnection(i)