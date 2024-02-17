import cv2  # Импорт библиотеки OpenCV для работы с изображениями и видео
import pyautogui  # Импорт библиотеки PyAutoGUI
import mediapipe as mp  # Импорт библиотеки Mediapipe для работы с руками и ключевыми точками
from mouse_action import events  # Импорт пользовательских событий
from mouse import events2

# Класс для представления позиции на изображении
class Position:

    def __init__(self, x, y):
        self.x = x  # Координата X позиции
        self.y = y  # Координата Y позиции

# Класс для представления сустава
class Joint:

    def __init__(self):
        self.position      = Position(0, 0)  # Текущая позиция сустава
        self.position_prev = Position(0, 0)  # Предыдущая позиция сустава

    # Обновление позиции сустава
    def update_position(self, new_joint_position):
        self.position_prev = self.position  # Сохранение предыдущей позиции
        self.position      = Position(new_joint_position.x, new_joint_position.y)  # Обновление текущей позиции

# Класс для представления руки
class Hand:

    def __init__(self):
        self.joints = {}  # Словарь для хранения суставов руки
        for id in range(21):
            self.joints[id] = Joint()  # Инициализация каждого сустава

    # Обновление позиций всех суставов руки
    def update_joints_position(self, new_joints_position):
        for id in range(21):
            new_joint_position = new_joints_position[id]  # Получение новой позиции сустава
            self.joints[id].update_position(new_joint_position)  # Обновление позиции сустава

# Получение размеров экрана
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

if __name__ == '__main__':
    hand = Hand()  # Создание объекта руки
    cap = cv2.VideoCapture(0)  # Инициализация видеозахвата с камеры
    hands = mp.solutions.hands.Hands(max_num_hands=1)  # Инициализация модели Mediapipe для обнаружения рук
    draw = mp.solutions.drawing_utils  # Утилиты для рисования на изображении

    while True:
        
        if cv2.waitKey(1) & 0xFF == 27:  # Проверка на нажатие клавиши Esc для завершения программы
            break

        success, image = cap.read()  # Захват кадра с камеры
        image = cv2.flip(image, 1)  # Отражение изображения
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Преобразование изображения из BGR в RGB
        results = hands.process(imageRGB)  # Обработка изображения моделью Mediapipe
        joints_position = {}  # Словарь для хранения позиций суставов
        
        if results.multi_hand_landmarks:  # Если на изображении обнаружены руки
            for handLms in results.multi_hand_landmarks:
                for id, landmarks in enumerate(handLms.landmark):  # Перебор всех ключевых точек руки
                    h, w, c = image.shape
                    frameR = 75 # Регулирование размера рамки для отслеживания рук
                    cv2.rectangle(image, (frameR, frameR), (w - frameR, h - frameR), (255, 0, 0), 2) # Рисование прямоугольника на изображении
                    cx, cy = int(landmarks.x * w), int(landmarks.y * h)
                    joints_position[id] = Position(cx, cy)  # Сохранение позиции сустава

                hand.update_joints_position(joints_position)  # Обновление позиций всех суставов руки
                for event in events:
                    event.try_do_action(hand)  # Попытка выполнения действия события для руки
                draw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)  # Рисование ключевых точек руки и соединяющих их линий
                
                for event2 in events2:
                    event2.try_do_action(hand)  # Попытка выполнения действия события для руки

        cv2.imshow("Hand", image)  # Отображение изображения с рисунками