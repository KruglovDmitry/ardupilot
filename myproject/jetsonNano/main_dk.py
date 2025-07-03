from dronekit import connect, VehicleMode, LocationGlobalRelative
import socket
import time
import sys
sys.path.insert(1, r'/home/dima/Desktop/ArduPilot/ardupilot/myproject/functions')
from connection import getPort

#Start SITL if no connection string specified
baud_rate = 57600
connection_string = getPort('jetsonNano')
vehicle = connect(connection_string, baud = baud_rate, wait_ready=True, timeout=30)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)



try:
    # Arm and take off to altitude of 5 meters
    arm_and_takeoff(5)

    time.sleep(5)
    # Landing
    vehicle.mode = VehicleMode("LAND")

            
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
print("Completed")