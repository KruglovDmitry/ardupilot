import sys
import math
import time
from pymavlink import mavutil

sys.path.insert(1, r'/home/dima/Desktop/ArduPilot/ardupilot/myproject/functions')
from set_params import subscribe_ask
from read_cmd import get_ask, handle_response
from connection import getPort
from arm import arm_copter
from change_mode import set_mode
from take_off import take_off_long, take_off_trottle, arm_and_takeoff_nogps, send_attitude_target, to_quaternion

# Create connection
master = mavutil.mavlink_connection(getPort('raspberryPi'), mavlink_version=2)

# Subscribe on ask commands
subscribe_ask(master)

# Choose mode
# 'GUIDED' - с отключением GPS в параметрах
# 'GUIDED_NOGPS' - отсутствует в прошивке
# 'FFLOWHOLD' - отсутствует в прошивке (ореинтация по оптическому потоку)
# 'POSHOLD' - есть но не позволяет совершать ARM (ореинтация по маякам)
# 'STABILIZE' - позволяет совершать ARM, который отключается через определенное время
# 'ALT_HOLD' - при ARM вращает двигателями интенсивнее и не останавливает их, пока не поменять режим
# 'ACRO' - ARM аналогично стабилизированному, но по факту нет стабилизации (акробатика)
set_mode(master, 'STABILIZE')

# Arm
armed = arm_copter(master)

# Give the autopilot time to initialize
time.sleep(2)  

#Take Off
if armed:
    #arm_and_takeoff_nogps(master, 1)
    use_yaw_rate = False
    duration = 5
    start = time.time()
    while time.time() - start < duration:
        master.mav.set_attitude_target_encode(
            0,                       # time_boot_ms
            1,                       # target_system
            1,                       # target_component
            0b10111000,              # Игнорировать ВСЕ, кроме thrust (бит 7 = 1)
            to_quaternion(0, 0, 0),  # Кватернион (не используется из-за маски)
            0, 0, 0,                # roll_rate, pitch_rate, yaw_rate (не используются)
            0.8                     # thrust (0.7–0.9 для взлёта)
        )
        handle_response(master)
        time.sleep(0.1)

