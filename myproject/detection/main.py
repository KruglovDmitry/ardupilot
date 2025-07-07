import cv2 # Импорт cv2 обязательно перед torch
import torch
import numpy as np
from utils import count_fps  # Проверьте, что эта функция определена корректно

print(f'Open cv version - {cv2.__version__}')
print(f'Torch version - {torch.__version__}')

# Инициализация переменных
prev_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# Загрузка модели YOLOv5
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Открытие веб-камеры (обычно 0)
cap = cv2.VideoCapture('/home/dima/Desktop/ArduPilot/ardupilot/myproject/detection/samples/84.mp4')

# Основной цикл
while cap.isOpened():
    success, img = cap.read()
    if not success:  # Проверка успешного чтения кадра
        break

    img = cv2.resize(img, (640, 480))  # Изменение размера кадра

    # Выполнение инференса
    #results = model(img)

    #for i in results.xyxy[0]:  # Обработка результатов
    #    x, y, x1, y1, name = int(i[0].item()), int(i[1].item()), int(i[2].item()), int(i[3].item()), results.names[int(i[5].item())]
    #    cv2.putText(img, f"{name}", (x-3, y-3), font, 0.3, (100, 255, 0), 1, cv2.LINE_AA)
    #    cv2.rectangle(img, (x, y), (x1, y1), (0, 155, 255), 1)

    current_fps, prev_frame_time = count_fps(prev_frame_time)
    cv2.putText(img, f"FPS - {current_fps}", (5, 20), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Webcam", img)  # Показ кадра

    if cv2.waitKey(1) & 0xFF == 27:  # Выход при нажатии Esc
        break

cap.release()  # Освобождение ресурсов
cv2.destroyAllWindows()