from pymavlink import mavutil

def take_off_long(master, alt = 1.0):

    print(f'Начало долгого взлета на высоту {alt}')
    # Взлет на указанную высоту
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0, 0, 0, alt
    )