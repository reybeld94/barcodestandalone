# clockout.py
import time
import pygetwindow as gw
import pyperclip
import keyboard
from PIL import ImageGrab
import numpy as np
from utils.modals import qty_modal_ref, show_qty_modal_in_mainloop
from utils.windows import activar_ventana
from utils.input import safe_click, safe_write, safe_press_enter, safe_hotkey
from utils.hook_control import stop_hook, start_hook
import utils.hook_listener as hook_listener

def esperar_color(bbox, color_fn, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if color_fn(bbox):
            return True
        time.sleep(0.3)
    return False

def hacer_clockout(user_code, wo_number, ctx):
    try:
        root = qty_modal_ref.get("root")
        if root and root.winfo_exists():

            root.after(0, root.destroy)
        qty_modal_ref["root"] = None
        time.sleep(0.2)
    except Exception as e:
        qty_modal_ref["root"] = None

    try:
        ventanas = gw.getWindowsWithTitle("Mie Kiosk")
        if not ventanas:
            return "❌ No se encontró ventana con título 'Mie Kiosk'"

        win = ventanas[0]
        activar_ventana(win)

        safe_click(161, 57)
        if not esperar_color((735, 454, 819, 475), es_amarillo):
            return "❌ No aparece login"
        safe_click(709, 466)
        safe_hotkey("ctrl", "a")
        safe_hotkey("backspace")
        safe_click(709, 466)
        safe_write(user_code)
        safe_press_enter()

        if not esperar_color((635, 819, 679, 938), es_blanco):
            return "❌ No aparece job listing"

        safe_click(825, 274)
        safe_write(wo_number)

        if not esperar_color((106, 298, 124, 310), es_azul):
            return "❌ No aparece logout"
        safe_click(111, 300)

        if not esperar_color((761, 332, 791, 349), es_gris):
            return "❌ No aparece ventana gris"

        safe_click(839, 441)

        if not esperar_color((776, 369, 814, 397), es_amarillo):
            return "❌ No aparece ventana amarilla"

        stop_hook()

        if ctx.get("root"):
            ctx["root"].after(0, lambda: show_qty_modal_in_mainloop(ctx["root"]))

        print("⌨️ Esperando que el usuario presione ENTER...")
        keyboard.wait("enter")
        print("✅ Enter recibido")

        while qty_modal_ref["root"]:
            time.sleep(0.1)

        start_hook(hook_listener.on_key)

        safe_click(839, 441)
        safe_hotkey("ctrl", "a")
        safe_hotkey("ctrl", "c")
        time.sleep(0.3)
        texto = pyperclip.paste()

        try:
            qty = float(texto.strip())
        except ValueError:
            return f"❌ No se pudo interpretar la cantidad: '{texto}'"

        safe_click(1359, 490)
        safe_hotkey("ctrl", "a")
        safe_hotkey("ctrl", "c")
        time.sleep(0.3)
        texto = pyperclip.paste()

        try:
            remaining = float(texto.strip())
        except ValueError:
            return f"❌ No se pudo interpretar Remaining Qty: '{texto}'"

        time.sleep(0.1)
        if qty < remaining:
            status = "Incomplete"
            print("⚠️ Marcado como Incomplete")
            safe_click(759, 893)
        else:
            status = "Complete"
            print("✅ Marcado como Complete")
            safe_click(876, 900)

        safe_click(1881, 668)
        safe_click(161, 57)

        return f"✅ Clock Out '{status}' completado con qty={qty} vs remaining={remaining}"
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
