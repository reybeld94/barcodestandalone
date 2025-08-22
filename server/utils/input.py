import pyautogui
# from utils.hook_control import stop_hook, start_hook
# from utils.hook_listener import on_key


def safe_write(text, interval=0.001):
    # stop_hook()
    pyautogui.write(text, interval=interval)
    # start_hook(on_key)

def safe_press_enter():
    # stop_hook()
    pyautogui.press("enter")
    # start_hook(on_key)


def safe_click(x, y):
    # stop_hook()
    pyautogui.click(x, y)
    # start_hook(on_key)

def safe_hotkey(*args):
    # stop_hook()
    pyautogui.hotkey(*args)
    # start_hook(on_key)
