from pymavlink import mavutil
from MAVProxy.modules.mavproxy_link import preferred_ports

def getPort(board):

    if (board == 'raspberryPi'):
        ports = mavutil.auto_detect_serial(preferred_list=preferred_ports)
        port = ports[0].device
    elif (board== 'jetsonNano'):
        port = '/dev/ttyTHS1'
    elif (board == "SITL"):
        port = 'udp:127.0.0.1:14551'
    else:
        port = "Device not defound"

    print("Подключение к порту:", port)
    return port
