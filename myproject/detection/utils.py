import time

def count_fps(prev_frame_time):
    current_frame_time = time.time()
    fps = 1 / (current_frame_time - prev_frame_time)
    prev_frame_time = current_frame_time
    return fps, prev_frame_time