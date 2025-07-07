import cv2
import time
import face_recognition

def count_fps(prev_frame_time):
    current_frame_time = time.time()
    fps = 1 / (current_frame_time - prev_frame_time)
    prev_frame_time = current_frame_time
    return fps, prev_frame_time

def detect_faces(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    result = face_recognition.face_locations(rgb_small_frame)

    for face_location in result:
        print("Detection!!!")
        top, right, bottom, left = face_location

        # Scale back
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)