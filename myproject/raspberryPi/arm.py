"""
Example of how to Arm and Disarm an Autopilot with pymavlink
"""
# Import mavutil
from pymavlink import mavutil

def arm_copter(master):
    
    # Wait a heartbeat before sending commnds
    master.wait_heartbeat()

    # Arm
    # master.arducopter_arm() or:
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)

    # wait until arming confirmed (can manually check with master.motors_armed())
    print("Waiting for the vehicle to arm")
    master.motors_armed_wait()
    print('Armed!')