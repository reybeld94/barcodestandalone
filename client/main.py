
import threading
from queue import Queue
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk
from logic.commands import process_code
from data.log_writer import log_entry
import utils.hook_listener as hook_listener
from utils.hook_control import start_hook
from utils.hook_listener import on_key
import sys
from services.status_monitor import status_monitor
from services.api_client import api_client

ctx = {
    "procesando": False,
    "modal_active": False,
    "scan_listbox": None,
    "root": None  # Root de Tkinter se inyectará aquí
}

current_user = {"id": None}
waiting_for_action = {"active": False}

executing_command = False
scan_buffer = ""
timestamps = []

command_queue = Queue()

def command_worker():
    global executing_command
    while True:
        code = command_queue.get()
        executing_command = True
        try:
            process_code(code, current_user, waiting_for_action, ctx)
        except Exception as e:
            log_entry(f"❌ Error ejecutando comando: {str(e)}", "#ff0022")
        executing_command = False
        command_queue.task_done()

def create_image():
    image = Image.new('RGB', (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return image

def quit_app(icon, item):
    print("🛑 Cerrando app...")
    icon.stop()
    if ctx.get("root"):
        try:
            ctx["root"].destroy()
        except:
            pass
    sys.exit()

def run_systray():
    menu = Menu(MenuItem('Quit', quit_app))
    icon = Icon("BarcodeAgent", create_image(), "Barcode Agent", menu)
    threading.Thread(target=icon.run, daemon=True).start()


def cerrar_app():
    print("🛑 CTRL + X detected. Closing app.")
    if ctx.get("root"):
        try:
            ctx["root"].destroy()
        except:
            pass
    sys.exit()

if __name__ == "__main__":
    print("🟢 App iniciada. Verificando servidor...")

    # Verificar conectividad del servidor
    if not api_client.check_server_health():
        print("❌ Servidor no disponible. Asegúrate de que esté corriendo.")
        input("Presiona Enter para continuar de todas formas...")
    else:
        print("✅ Servidor conectado correctamente")

    # Iniciar monitor de status
    status_monitor.start_monitoring()

    root = tk.Tk()
    root.withdraw()  # Oculta ventana principal
    ctx["root"] = root

    hook_listener.command_queue = command_queue
    hook_listener.ctx = ctx
    hook_listener.current_user = current_user
    hook_listener.waiting_for_action = waiting_for_action

    start_hook(on_key)

    threading.Thread(target=command_worker, daemon=True).start()
    run_systray()


    root.mainloop()
