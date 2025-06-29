from pymavlink import mavutil
from MAVProxy.modules.mavproxy_link import preferred_ports

def getPort():
    ports = mavutil.auto_detect_serial(preferred_list=preferred_ports)
    port = ports[0].device
    print("Подключение к порту:", port)
    return port
