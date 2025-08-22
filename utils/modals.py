import tkinter as tk
import platform
import time

# Sonido en Windows
if platform.system() == "Windows":
    from winsound import Beep

    def play_alert_sound():
        for _ in range(3):
            Beep(1500, 100)
            Beep(1000, 100)
else:
    def play_alert_sound():
        pass

qty_modal_ref = {"root": None}

# ✅ ALERTA VISUAL SEGURA CON ctx
def show_alert(
    title="⚠️ SYSTEM ERROR",
    message="⚠️ UNABLE TO CLOCK IN\nPLEASE SCAN YOUR CODE AGAIN",
    duration=5,
    ctx=None
):
    def run_modal():
        play_alert_sound()

        modal = tk.Toplevel(ctx["root"] if ctx else None)
        modal.title(title)
        modal.overrideredirect(True)
        modal.attributes("-topmost", True)
        modal.configure(bg="red")

        screen_width = modal.winfo_screenwidth()
        screen_height = modal.winfo_screenheight()
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.4)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        modal.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(
            modal,
            text=message,
            font=("Arial", 36, "bold"),
            fg="white",
            bg="red",
            wraplength=window_width - 60,
            justify="center"
        )
        label.pack(expand=True, fill="both", padx=40, pady=40)

        def blink():
            current = label.cget("fg")
            label.config(fg="white" if current == "red" else "red")
            modal.after(500, blink)

        blink()

        # 🔥 OPCIONAL: cerrar también con Enter
        def cerrar_enter(event=None):
            if modal.winfo_exists():
                modal.destroy()

        modal.bind("<Return>", cerrar_enter)

        modal.after(int(duration * 1000), lambda: modal.destroy())

    # ✅ Si tienes root, úsalo con .after()
    if ctx and ctx.get("root"):
        ctx["root"].after(0, run_modal)
    else:
        # Fallback por si se usa sin contexto (no recomendado)
        import threading
        threading.Thread(target=run_modal, daemon=True).start()


def show_error_modal(message="⚠️ UNEXPECTED ERROR", duration=5, ctx=None):
    show_alert("❌ SYSTEM ERROR", message, duration, ctx)


def show_qty_modal_in_mainloop(root, message="Please type the quantity manually and press ENTER"):
    print("🟡 [MODAL] Iniciando modal de cantidad (mainloop-safe)...")

    if qty_modal_ref["root"]:
        try:
            if qty_modal_ref["root"].winfo_exists():
                qty_modal_ref["root"].destroy()
        except:
            pass
        qty_modal_ref["root"] = None

    try:
        modal = tk.Toplevel(root)
        qty_modal_ref["root"] = modal
        modal.title("Manual Qty Input")
        modal.overrideredirect(True)
        modal.configure(bg="yellow")
        modal.attributes("-topmost", True)

        screen_width = modal.winfo_screenwidth()
        window_width = int(screen_width * 0.9)
        window_height = 120
        x = (screen_width - window_width) // 2
        y = 50
        modal.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(
            modal,
            text=message,
            font=("Arial", 24, "bold"),
            fg="black",
            bg="yellow"
        )
        label.pack(expand=True, fill="both", padx=30, pady=10)

        def blink():
            current = label.cget("fg")
            label.config(fg="black" if current == "yellow" else "yellow")
            modal.after(250, blink)

        blink()

        def cerrar_enter(event=None):
            print("🟡 [MODAL] Enter presionado. Cerrando modal.")
            if modal.winfo_exists():
                modal.destroy()
                qty_modal_ref["root"] = None

        modal.bind("<Return>", cerrar_enter)

        def cerrar(event=None):
            print("🟡 [MODAL] Detectado movimiento para cerrar.")
            if modal.winfo_exists():
                modal.destroy()
                qty_modal_ref["root"] = None

        modal.bind("<Motion>", cerrar)

        def kill_all():
            print("🟡 [MODAL] Timeout. Cerrando modal.")
            if modal.winfo_exists():
                modal.destroy()
            qty_modal_ref["root"] = None

        modal.after(10000, kill_all)

    except Exception as e:
        print("❌ [MODAL ERROR]:", str(e))
