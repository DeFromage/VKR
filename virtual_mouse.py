import cv2 as cv  # Импорт библиотеки OpenCV под псевдонимом cv
import mediapipe as mp  # Импорт библиотеки Mediapipe под псевдонимом mp
import numpy as np  # Импорт библиотеки NumPy под псевдонимом np
import pyautogui as pg  # Импорт библиотеки PyAutoGUI под псевдонимом pg

# Инициализация камеры
cam = cv.VideoCapture(0)

# Инициализация модели Mediapipe для обнаружения рук
mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

# Получение размеров экрана
screenWidth, screenHeight = pg.size()
print(screenWidth, screenHeight)

# Размеры рамки для отслеживания рук
frameR = 75

# Идентификаторы кончиков пальцев
tipid = [4, 8, 12, 16, 20]

# Счетчик кликов
clk = 1

while True:
    # Чтение кадра с камеры
    success, img = cam.read()

    # Отражение изображения
    img = cv.flip(img, 1)

    h, w, c = img.shape

    # Преобразование цветов из BGR в RGB
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Рисование прямоугольника на изображении
    cv.rectangle(img, (frameR, frameR), (w - frameR, h - frameR), (255, 0, 0), 2)

    if results.multi_hand_landmarks:
        # Определение, какая рука видна на изображении
        hand_label = results.multi_handedness[0].classification[0].label
        if hand_label == "Right":
            lmlist = []

            # Получение координат ключевых точек руки
            for handLms in results.multi_hand_landmarks:
                for id, landmarks in enumerate(handLms.landmark):
                    cx, cy = int(landmarks.x * w), int(landmarks.y * h)
                    lmlist.append([id, cx, cy])
                    mpDraw.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)  # Рисование ключевых точек руки и соединяющих их линий
            # Обработка жестов пальцев
            fingers = []
            if lmlist[tipid[0]][1] < lmlist[tipid[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmlist[tipid[id]][2] < lmlist[tipid[id] - 3][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Управление мышью
            if fingers == [0, 1, 1, 0, 0]:
                cv.circle(img, (lmlist[12][1], lmlist[12][2]), 10, (0, 0, 255), cv.FILLED)

                X = np.interp(lmlist[12][1], (frameR, w - frameR), (0, screenWidth))
                Y = np.interp(lmlist[12][2], (frameR, h - frameR), (0, screenHeight))

                length = abs(lmlist[8][1] - lmlist[12][1])

                pg.moveTo(X, Y, duration=0.3)

                # Клик мыши
                if lmlist[8][2] > lmlist[7][2] and clk > 0:
                    pg.click()
                    clk = -1
                elif lmlist[8][2] < lmlist[7][2]:
                    clk = 1
    
    # Отображение изображения с камеры
    cv.imshow("webcam", img)

    # Выход из цикла при нажатии клавиши Esc
    if cv.waitKey(1) & 0xFF == 27:
        break

# Закрытие окон OpenCV
cv.destroyAllWindows()
