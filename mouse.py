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
def click_check(hand):
    
    condition4 = hand.joints[20].position.y > hand.joints[17].position.y
    condition5 = hand.joints[16].position.y > hand.joints[13].position.y
    condition6 = hand.joints[12].position.y > hand.joints[9].position.y
    condition7 = abs(hand.joints[4].position.x - hand.joints[7].position.x) < 30
    
    return condition4 and condition5 and condition6 and condition7

# Действие при истинном условии "вверх"
def click_true_action(hand):
    pyautogui.mouseDown(button='left')
    
def click_false_action(hand):
    pyautogui.mouseUp(button='left')

# Создание объекта события "вверх"
mouse_click = Event(click_check, click_true_action, click_false_action)

# Добавление объекта события "вверх" в список events
events2 = [mouse_click]