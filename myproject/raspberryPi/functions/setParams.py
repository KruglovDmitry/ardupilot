from pymavlink import mavutil
from read_cmd import handle_response

def disable_GPS(master):
    
    print('Send cmd to disable GPS')
    param_set = connection.mav.param_set_send(
        master.target_system,
        master.target_component,
        b'EK2_GPS_TYPE',
        0,  # 0 = GPS отключен
        mavutil.mavlink.MAV_PARAM_TYPE_INT8
    )

    handle_response(master)

