import time
import math
from pymavlink import mavutil
from read_cmd import handle_response

def take_off_long(master, alt = 1.0):

    print(f'Начало долгого взлета на высоту {alt}')
    # Взлет на указанную высоту
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, alt
    )

def take_off_trottle(master, alt = 1.0):
    
    print(f"Взлёт на {alt} м...")
    start_time = time.time()
    while time.time() - start_time < 5:  # Таймаут 5 сек
        timestamp = int((time.time() - start_time) * 1e9) & 0xFFFFFFFF

        # Установка газа (thrust) и тангажа
        master.mav.set_attitude_target_send(
            timestamp,
            master.target_system,
            master.target_component,
            0b00000000,  # type_mask (игнорировать attitude)
            [0, 0, 0, 0],  # attitude quaternion (не используется)
            0, 0, 0,  # body rates
            0.7)  # thrust (0.5-0.7 для взлёта)
        
        handle_response(master)
        time.sleep(0.1)
    
    print("Взлёт завершён")
    return True

def arm_and_takeoff_nogps(master, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = get_current_altitude(master)
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(master, thrust = thrust)
        time.sleep(0.2)

def get_current_altitude(master):
    """
    Возвращает текущую относительную высоту в метрах (от точки взлёта)
    :param connection: MAVLink-соединение
    :return: Высота в метрах или None при ошибке
    """
    # Запрашиваем актуальные данные
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        1,  # rate_hz
        1   # start/stop
    )
    
    # Ждём сообщение GLOBAL_POSITION_INT
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=3)
    
    if msg:
        return msg.relative_alt / 1000  # Переводим из мм в метры
    return None

def set_attitude(master, roll_angle = 0.0, pitch_angle = 0.0,
                 yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                 thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent more often than every
    second, as an ATTITUDE_TARGET order has a timeout of 1s.
    In AC3.2.1 and earlier the specified attitude persists until it is canceled.
    The code below should work on either version.
    Sending the message multiple times is the recommended way.
    """
    send_attitude_target(master, roll_angle, pitch_angle,
                         yaw_angle, yaw_rate, False,
                         thrust)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(master, roll_angle, pitch_angle,
                             yaw_angle, yaw_rate, False,
                             thrust)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(master, 0, 0,
                         0, 0, True,
                         thrust)

def send_attitude_target(master, roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):
    """
    use_yaw_rate: the yaw can be controlled using yaw_angle OR yaw_rate.
                  When one is used, the other is ignored by Ardupilot.
    thrust: 0 <= thrust <= 1, as a fraction of maximum vertical thrust.
            Note that as of Copter 3.5, thrust = 0.5 triggers a special case in
            the code for maintaining current altitude.
    """
    if yaw_angle is None:
        # this value may be unused by the vehicle, depending on use_yaw_rate
        yaw_angle = get_attitude(master)['yaw'] if get_attitude(master) != None else 0
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    master.mav.set_attitude_target_encode(
        0, # time_boot_ms
        1, # Target system
        1, # Target component
        0b00000000 if use_yaw_rate else 0b00000100,
        to_quaternion(roll_angle, pitch_angle, yaw_angle), # Quaternion
        0, # Body roll rate in radian
        0, # Body pitch rate in radian
        math.radians(yaw_rate), # Body yaw rate in radian/second
        thrust  # Thrust
    )

def get_attitude(master):
    """
    Возвращает текущие углы ориентации в радианах
    :param connection: MAVLink-соединение
    :return: Словарь с углами {'roll', 'pitch', 'yaw'} в радианах или None при ошибке
    """
    msg = master.recv_match(type='ATTITUDE', blocking=True, timeout=3)
    if msg:
        return {
            'roll': msg.roll,
            'pitch': msg.pitch,
            'yaw': msg.yaw
        }
    return None


def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]
