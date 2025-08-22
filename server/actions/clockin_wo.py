# clockin_wo.py
import time
import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
import numpy as np
from actions.clockout import es_blanco, es_azul, es_gris
from utils.windows import activar_ventana
from utils.input import safe_click, safe_write, safe_press_enter, safe_hotkey

def esperar_color(bbox, color_fn, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if color_fn(bbox):
            return True
        time.sleep(0.3)
    return False

def hacer_clockin_workorder(user_code, operation, part_number, wo_number):
    try:
        print(f"➡️ ClockIn WO | User: {user_code}, OP: {operation}, Part: {part_number}, WO: {wo_number}")
        ventanas = gw.getWindowsWithTitle("Mie Kiosk")
        if not ventanas:
            return "❌ No se encontró ventana con título 'Mie Kiosk'"

        win = ventanas[0]
        activar_ventana(win)
        time.sleep(1)

        pyautogui.click(153, 54)  # home_btn

        if not esperar_color((735, 454, 819, 475), es_amarillo):
            return "❌ No aparece el field login"
        pyautogui.click(707, 465)
        safe_hotkey("ctrl", "a")
        safe_hotkey("backspace")
        pyautogui.click(707, 465)
        safe_write(user_code)
        safe_press_enter()

        if not esperar_color((641, 836, 682, 923), es_blanco):
            return "❌ No aparece job listing"
        pyautogui.click(309, 775)

        if not esperar_color((1440, 888, 1487, 913), es_blanco):
            return "❌ No aparece campo WO"

        pyautogui.click(882, 152)
        safe_write(wo_number)

        pyautogui.click(1337, 154)
        safe_write(part_number)

        pyautogui.click(1532, 154)
        safe_write(operation)



        if not esperar_color((546, 172, 567, 190), es_azul):
            return "❌ No aparece login_btn"
        pyautogui.click(524, 179)

        time.sleep(2)

        # Buscar ventanas que contengan "Confirm"
        ventanas_confirm = [w for w in gw.getAllTitles() if "Confirm" in w]

        if ventanas_confirm:
            print("✅ Ventana 'Confirm' detectada!")
            pyautogui.click(1013, 595)
        else:
            print("❌ No se detectó ventana 'Confirm'")

        if not esperar_color((1387, 457, 1460, 484), es_gris):
            return "❌ No aparece ventana gris"
        time.sleep(2)
        pyautogui.click(679, 838)

        pyautogui.click(153, 54)
        return "✅ WO Clock In completado"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def es_azul(bbox, threshold=0.6):
    img = ImageGrab.grab(bbox)
    pixels = np.array(img)
    r = pixels[:, :, 0]
    g = pixels[:, :, 1]
    b = pixels[:, :, 2]
    azul_mask = (b > 100) & (b > r + 30) & (b > g + 30)
    porcentaje_azul = azul_mask.sum() / azul_mask.size
    print(f"🔵 Área azul detectada: {porcentaje_azul:.2%}")
    return porcentaje_azul >= threshold


def es_gris(bbox, threshold=0.6):
    img = ImageGrab.grab(bbox)
    pixels = np.array(img)
    r = pixels[:, :, 0].astype(int)
    g = pixels[:, :, 1].astype(int)
    b = pixels[:, :, 2].astype(int)
    gris_mask = (abs(r - g) < 15) & (abs(r - b) < 15) & (abs(g - b) < 15)
    porcentaje_gris = gris_mask.sum() / gris_mask.size
    print(f"⬜ Área gris detectada: {porcentaje_gris:.2%}")
    return porcentaje_gris >= threshold


def es_amarillo(bbox, threshold=0.6):
    img = ImageGrab.grab(bbox)
    pixels = np.array(img)
    r = pixels[:, :, 0].astype(int)
    g = pixels[:, :, 1].astype(int)
    b = pixels[:, :, 2].astype(int)
    amarillo_mask = (r > 200) & (g > 200) & (b < r - 20) & (b < g - 20)
    porcentaje_amarillo = amarillo_mask.sum() / amarillo_mask.size
    print(f"🟡 Área amarilla detectada: {porcentaje_amarillo:.2%}")
    return porcentaje_amarillo >= threshold

def es_blanco(bbox, threshold=0.6):
    img = ImageGrab.grab(bbox)
    pixels = np.array(img)
    r = pixels[:, :, 0].astype(int)
    g = pixels[:, :, 1].astype(int)
    b = pixels[:, :, 2].astype(int)
    blanco_mask = (r > 220) & (g > 220) & (b > 220)
    porcentaje_blanco = blanco_mask.sum() / blanco_mask.size
    print(f"⬜ Área blanca detectada: {porcentaje_blanco:.2%}")
    return porcentaje_blanco >= threshold
