import sys
# Import mavutil
from pymavlink import mavutil
from read_cmd import handle_response

# Create the connection
def set_mode(master, mode = 'STABILIZE'):
    # Wait a heartbeat before sending commands
    master.wait_heartbeat()

    # Check if mode is available
    if mode not in master.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(master.mode_mapping().keys()))
        sys.exit(1)

    # Get mode ID
    mode_id = master.mode_mapping()[mode]
    print(f'Mode id - {mode_id}')

    # Set new mode
    # master.mav.command_long_send(
    #    master.target_system, master.target_component,
    #    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    #    0, mode_id, 0, 0, 0, 0, 0) or:
    # master.set_mode(mode_id) or:
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)

    handle_response(master)