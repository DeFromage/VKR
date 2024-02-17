import pyautogui  # Импорт библиотеки PyAutoGUI

class Keyboard:
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
def up_check(hand):
    return hand.joints[4].position.x > hand.joints[3].position.x

# Действие при истинном условии "вверх"
def up_true_action(hand):
    pyautogui.keyDown('up', _pause=False)

# Действие при ложном условии "вверх"
def up_false_action(hand):
    pyautogui.keyUp('up', _pause=False)

# Создание объекта события "вверх"
up_event = Keyboard(up_check, up_true_action, up_false_action)

# Добавление объекта события "вверх" в список keyboard
keyboard = [up_event]

# Функция проверки условия "вниз"
def down_check(hand):
    return abs(hand.joints[8].position.x - hand.joints[12].position.x) > 40

# Действие при истинном условии "вниз"
def down_true_action(hand):
    pyautogui.keyDown('down', _pause=False)

# Действие при ложном условии "вниз"
def down_false_action(hand):
    pyautogui.keyUp('down', _pause=False)

# Создание объекта события "вниз"
down_event = Keyboard(down_check, down_true_action, down_false_action)

# Добавление объекта события "вниз" в список keyboard
keyboard.append(down_event)