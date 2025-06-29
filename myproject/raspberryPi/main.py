import time
from pymavlink import mavutil
from connection import getPort
from arm import arm_copter
from change_mode import set_mode

# Create the connection
master = mavutil.mavlink_connection(getPort())

# Choose mode
set_mode(master) # need- 'GUIDED_NOGPS'

# Arm
arm_copter(master)
