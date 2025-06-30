from pymavlink import mavutil
import time

# Подключение к Pixhawk (замените порт на свой)
print("Попытка подключения")
connection = mavutil.mavlink_connection('udp:127.0.0.1:14551')  # SITL

# Ожидание подключения
connection.wait_heartbeat()
print("Подключено к Pixhawk!")