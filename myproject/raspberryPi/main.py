import sys
import time
from pymavlink import mavutil

sys.path.insert(1, r'/home/dima/Desktop/ArduPilot/ardupilot/myproject/raspberryPi/functions')
from connection import getPort
from arm import arm_copter
from change_mode import set_mode

# Create the connection
master = mavutil.mavlink_connection(getPort())

# Choose mode
# 'GUIDED' - с отключением GPS в параметрах
# 'GUIDED_NOGPS' - отсутствует в прошивке
# 'FFLOWHOLD' - отсутствует в прошивке (ореинтация по оптическому потоку)
# 'POSHOLD' - есть но не позволяет совершать ARM (ореинтация по маякам)
# 'STABILIZE' - позволяет совершать ARM, который отключается через определенное время
# 'ALT_HOLD' - при ARM вращает двигателями интенсивнее и не останавливает их, пока не поменять режим
# 'ACRO' - ARM аналогично стабилизированному, но по факту нет стабилизации (акробатика)
set_mode(master, 'GUIDED') 

# Arm
arm_copter(master)
