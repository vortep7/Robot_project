import cv2
import numpy as np


# Функция для поиска желтого объекта и определения его координат
def find_yellow_object(frame):
    # Преобразование изображения в цветовое пространство HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Определение диапазона желтого цвета в HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Создание маски для желтого объекта
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Нахождение контуров желтого объекта
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Найден желтый объект
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:
            # Вычисление центра желтого объекта
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            return cx, cy
    return None, None



def find_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)   #делаю маску

    # Нахождение контуров зеленого объекта
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments['m00'] != 0:
            # ищем центр
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            return cx, cy
    return None, None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()   #первая переменная просто тру хранит до момента окончания видео

    if not ret:
        break

    # Поиск желтого объекта и получение его координат
    yellow_x, yellow_y = find_yellow_object(frame)

    # Поиск зеленого объекта и получение его координат
    green_x, green_y = find_object(frame)

    if yellow_x is not None and yellow_y is not None:
        # Отображение желтого объекта и системы координат
        cv2.circle(frame, (yellow_x, yellow_y), 10, (0, 255, 255), -1)  # Желтый круг на объекте
        cv2.line(frame, (yellow_x, yellow_y), (yellow_x + 50, yellow_y), (0, 255, 255), 2)  # Ось X
        cv2.line(frame, (yellow_x, yellow_y), (yellow_x, yellow_y + 50), (0, 255, 255), 2)  # Ось Y

    if green_x is not None and green_y is not None:
        # Отображение зеленого объекта и его координат в системе координат желтого объекта
        cv2.circle(frame, (green_x, green_y), 10, (0, 255, 0), -1)  # Зеленый круг на объекте
        if yellow_x is not None and yellow_y is not None:
            # Вычисление координат зеленого объекта относительно желтого объекта
            relative_x = green_x - yellow_x
            relative_y = green_y - yellow_y
            cv2.putText(frame, f'Relative: ({relative_x}, {relative_y})', (yellow_x + 10, yellow_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Object Tracking', frame)

    # Для выхода из программы нажмите клавишу 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
