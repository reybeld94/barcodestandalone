import time
import pyautogui
import pygetwindow as gw
from utils.images import esperar_y_localizar
from utils.windows import activar_ventana


def hacer_clockin(user_code):
    try:
        print(f"➡️ ClockIn para usuario: {user_code}")
        ventanas = gw.getWindowsWithTitle("Mie Kiosk")
        if not ventanas:
            return "❌ No se encontró ventana con título 'Mie Kiosk'"

        win = ventanas[0]
        activar_ventana(win)
        time.sleep(1)

        login = esperar_y_localizar("images/loginbox.png")
        if not login:
            return "❌ loginbox.png no encontrado"

        pyautogui.click(login.x + 50, login.y + 10)
        time.sleep(0.3)
        pyautogui.write(user_code)
        pyautogui.press("enter")
        time.sleep(2)

        clock_btn = esperar_y_localizar("images/clockinbtn.png")
        if not clock_btn:
            return "❌ clockinbtn.png no encontrado"

        pyautogui.click(clock_btn.x + 20, clock_btn.y + 10)
        time.sleep(2)

        home_btn = pyautogui.locateCenterOnScreen("images/home_btn.png", confidence=0.8)
        if home_btn:
            pyautogui.click(home_btn)

        return "✅ Clock In hecho"

    except Exception as e:
        return f"❌ Error: {str(e)}"
