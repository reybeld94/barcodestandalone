import os
from datetime import datetime

def log_entry(msg, color="#000", listbox=None):
    """Muestra el mensaje en consola y guarda el log."""
    print(msg)
    save_log_line(msg)

def save_log_line(msg):
    """Guarda el mensaje con timestamp en un archivo log diario."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{today}_log.txt")
    timestamp = datetime.now().strftime("%I:%M:%S %p").lstrip("0")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
