import traci
import math

# Initialize SUMO simulation
sumoBinary = "sumo-gui"  # Use "sumo" for non-GUI simulation
sumoCmd = [sumoBinary, "-c", "tinker-final.sumocfg"]  # Replace with your SUMO config file
traci.start(sumoCmd)

# Function to calculate distance between two vehicles
def get_distance(veh1, veh2):
    pos1 = traci.vehicle.getPosition(veh1)
    pos2 = traci.vehicle.getPosition(veh2)
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# Function to control speeds based on distance, including emergency braking and stopping the leader
def control_distance(leader, follower):
    if leader in traci.vehicle.getIDList() and follower in traci.vehicle.getIDList():
        # Get current distance between vehicles
        distance = get_distance(leader, follower)
        print(f"Distance between {leader} and {follower}: {distance:.2f} meters")  # Log distance
        
        # Emergency braking if the distance is critically low
        if distance < 5:
            print(f"EMERGENCY BRAKE: {follower} too close to {leader}!")
            traci.vehicle.setSpeed(follower, 0)  # Stop the follower immediately
        
        # Adjust speed based on distance thresholds
        elif distance < 15:  # Too close
            traci.vehicle.setSpeed(follower, 2)  # Slow down follower
            traci.vehicle.setSpeed(leader, 8)    # Speed up leader
        elif distance > 50:  # Too far
            traci.vehicle.setSpeed(follower, 8)  # Speed up follower
            traci.vehicle.setSpeed(leader, 2)    # Slow down leader
        elif distance > 70:  # Distance is too large, stop the leader
            print(f"Leader {leader} stopped due to too large distance with {follower}")
            traci.vehicle.setSpeed(leader, 0)  # Stop the leader
        else:  # Optimal distance
            traci.vehicle.setSpeed(follower, 5)  # Maintain normal speed
            traci.vehicle.setSpeed(leader, 5)

# Function to simulate varying environmental conditions
def adjust_for_environment(weather_condition):
    if weather_condition == "rain":
        print("Adverse weather detected: Slowing all vehicles.")
        for veh in traci.vehicle.getIDList():
            current_speed = traci.vehicle.getSpeed(veh)
            traci.vehicle.setSpeed(veh, max(1, current_speed * 0.7))  # Reduce speed by 30%
    elif weather_condition == "fog":
        print("Fog detected: Reducing visibility and slowing down vehicles.")
        for veh in traci.vehicle.getIDList():
            current_speed = traci.vehicle.getSpeed(veh)
            traci.vehicle.setSpeed(veh, max(1, current_speed * 0.5))  # Reduce speed by 50%
    elif weather_condition == "snow":
        print("Snow detected: Slowing down vehicles further.")
        for veh in traci.vehicle.getIDList():
            current_speed = traci.vehicle.getSpeed(veh)
            traci.vehicle.setSpeed(veh, max(1, current_speed * 0.4))  # Reduce speed by 60%
    else:
        print("Clear weather: Normal driving conditions.")
        # No adjustment for clear weather

# Main simulation loop
try:
    # Get weather condition from user input
    weather_condition = input("Enter weather condition (clear/rain/fog/snow): ").lower()

    while traci.simulation.getMinExpectedNumber() > 0:  # While there are active vehicles
        traci.simulationStep()  # Advance simulation by one step

        # Get the list of vehicles currently in the simulation
        active_vehicles = traci.vehicle.getIDList()

        # Control distances for the platoon
        if "leader1" in active_vehicles and "follower1" in active_vehicles:
            control_distance("leader1", "follower1")
        if "follower1" in active_vehicles and "follower2" in active_vehicles:
            control_distance("follower1", "follower2")
        if "leader2" in active_vehicles and "follower3" in active_vehicles:
            control_distance("leader2", "follower3")
        if "follower3" in active_vehicles and "follower4" in active_vehicles:
            control_distance("follower3", "follower4")

        # Simulate environmental adjustments based on input
        adjust_for_environment(weather_condition)

finally:
    traci.close()  # Close SUMO simulation properly
