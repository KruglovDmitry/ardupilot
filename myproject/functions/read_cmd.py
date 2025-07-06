import time
from pymavlink import mavutil

def handle_response(master):
    
    while True:
    # Wait for ACK command
    # Would be good to add mechanism to avoid endlessly blocking
    # if the autopilot sends a NACK or never receives the message
        msg = master.recv_match()
        
        if msg:
            msg = msg.to_dict()
            if msg['mavpackettype'] == 'COMMAND_ACK':
                # Continue waiting if the acknowledged command is not `set_mode
                if msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                    continue

                # Print the ACK result !
                print(mavutil.mavlink.enums['MAV_RESULT'][msg['result']].description)
                break

            elif msg['mavpackettype'] == 'STATUSTEXT':
                print(f"Status returned from flight controller - {msg['text']}")
                break

            else:
                print(msg)
                break

def get_ask(master, timeout=3):
    
    # Ожидание ответа
    start_time = time.time()
    while time.time() - start_time < timeout:
        msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=timeout)
        if msg and msg.command == cmd:
            print(f"ACK: {msg.result} ({(msg.result_param2)}")
            return msg
        time.sleep(0.1)
    
    print("Таймаут ожидания ACK")
    return None