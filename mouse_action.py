import pyautogui  # Импорт библиотеки PyAutoGUI
import numpy

class Event:
    def __init__(self, check_func, action_if_true, action_if_false):
        self.check_func = check_func
        self.action_if_true = action_if_true
        self.action_if_false = action_if_false

    def try_do_action(self, hand):
        if self.check_func(hand):
            if self.action_if_true:
                self.action_if_true(hand)
            return
        if self.action_if_false:
            self.action_if_false(hand)


# Функция проверки условия "вверх"
def tracking_check(hand):
    
    condition1 = hand.joints[20].position.y > hand.joints[17].position.y
    condition2 = hand.joints[16].position.y > hand.joints[13].position.y
    condition3 = hand.joints[12].position.y > hand.joints[9].position.y
    
    return condition1 and condition2 and condition3

# Действие при истинном условии "вверх"
def trckiang_true_action(hand):
    pyautogui.moveTo( hand.joints[8].position.x*4, hand.joints[8].position.y*4, duration=0)

# Создание объекта события "вверх"
mouse_tracking = Event(tracking_check, trckiang_true_action, 0)

# Добавление объекта события "вверх" в список events
events = [mouse_tracking]