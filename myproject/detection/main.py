import cv2 # Импорт cv2 обязательно перед torch
import torch
import numpy as np
from utils import count_fps  # Проверьте, что эта функция определена корректно
from ultralytics import YOLO

print(f'Open cv version - {cv2.__version__}')
print(f'Torch version - {torch.__version__}')

# Инициализация переменных
prev_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# Загрузка модели YOLOv5
model = YOLO('yolov5s.pt')

# Открытие веб-камеры (обычно 0)
cap = cv2.VideoCapture('/home/dima/Desktop/ArduPilot/ardupilot/myproject/detection/samples/84.mp4')

# Основной цикл
while cap.isOpened():
    success, img = cap.read()
    if not success:  # Проверка успешного чтения кадра
        break

    img = cv2.resize(img, (640, 480))  # Изменение размера кадра

    # Выполнение инференса
    results = model(img)
    result = results[0]   # Берём первый (и единственный) результат

    # Обработка боксов (новый формат)
    boxes = result.boxes.xyxy.cpu().numpy()  # [N, 4] — координаты в numpy
    classes = result.boxes.cls.cpu().numpy()  # [N] — классы
    confidences = result.boxes.conf.cpu().numpy()  # [N] — уверенность

    # Рисуем боксы и подписи
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = map(int, box)
        name = result.names[int(cls)]  # Имя класса

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{name} {conf:.2f}", (x1, y1 - 5), 
                   font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    current_fps, prev_frame_time = count_fps(prev_frame_time)
    cv2.putText(img, f"FPS - {current_fps}", (5, 20), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Webcam", img)  # Показ кадра

    if cv2.waitKey(1) & 0xFF == 27:  # Выход при нажатии Esc
        break

cap.release()  # Освобождение ресурсов
cv2.destroyAllWindows()
