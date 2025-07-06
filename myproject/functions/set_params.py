from pymavlink import mavutil
from read_cmd import handle_response

def disable_GPS(master):
    
    print('Send cmd to disable GPS')
    param_set = connection.mav.param_set_send(
        master.target_system,
        master.target_component,
        b'EK2_GPS_TYPE',
        0,  # 0 = GPS отключен
        mavutil.mavlink.MAV_PARAM_TYPE_INT8)

def subscribe_ask(master):

    print('Subscribre on ask commands')
    master.mav.param_set_send(
    master.target_system,
    master.target_component,
    b'SERIAL0_OPTIONS',
    4, # 4 = Always send COMMAND_ACK
    mavutil.mavlink.MAV_PARAM_TYPE_INT8)