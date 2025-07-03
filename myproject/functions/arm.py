from pymavlink import mavutil
from read_cmd import handle_response

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

    handle_response(master)
    
    # wait until arming confirmed (can manually check with master.motors_armed())
    print("Waiting for the vehicle to arm")
    master.motors_armed_wait()
    print('Armed!')
    
    return True