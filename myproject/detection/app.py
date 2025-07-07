import cv2
import time
from utils import count_fps, detect_faces

# Main #
print(f"App started, for quit press Esc")

prev_frame_time = 0
cap = cv2.VideoCapture('/home/dima/Desktop/ArduPilot/ardupilot/myproject/detection/samples/84.mp4')
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while (cap.isOpened()): 

    success, image = cap.read()
    image = cv2.resize(image, (800, 600))
    current_fps, prev_frame_time = count_fps(prev_frame_time)
    cv2.putText(image, f"{current_fps} {width}X{height}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

    detect_faces(image)
    cv2.imshow("Video", image)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()