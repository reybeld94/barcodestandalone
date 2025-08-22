import time
import pygetwindow as gw
import pyautogui

def activar_ventana(ventana):
    """
    Trae la ventana al frente, la maximiza si es necesario y la enfoca.
    Compatible con casos donde la ventana está abierta pero detrás de otras.
    """
    try:
        if ventana.isMinimized:
            ventana.restore()
            time.sleep(0.3)

        # Maximizar si no lo está
        if not ventana.isMaximized:
            ventana.maximize()
            time.sleep(0.3)

        # Activar (traer al frente)
        ventana.activate()
        time.sleep(0.3)

        box = ventana.box  # (left, top, width, height)
        x = box.left + 50
        y = box.top + 50
        pyautogui.moveTo(x, y)
        pyautogui.click()  # clic para asegurar foco

    except Exception as e:
        print(f"⚠️ Error activando ventana: {e}")
