import time
from pymavlink import mavutil
from MAVProxy.modules.mavproxy_link import preferred_ports

ports = mavutil.auto_detect_serial(preferred_list=preferred_ports)
port = ports[0].device
print("Подключение к порту:", port)


# Подключение к Pixhawk (замените порт на свой)
connection = mavutil.mavlink_connection(port, baud=57600)  # USB
# connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')  # SITL

# Ожидание подключения
connection.wait_heartbeat()
print("Подключено к Pixhawk!")

# Отправка команды на перезагрузку (параметр 1 = перезагрузка автопилота)
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
    0,  # confirmation
    1,  # reboot autopilot (1 = перезагрузка, 2 = shutdown)
    0, 0, 0, 0, 0, 0  # остальные параметры не используются
)

print("Команда на перезагрузку отправлена!")
time.sleep(2)  # Даём время на выполнение
