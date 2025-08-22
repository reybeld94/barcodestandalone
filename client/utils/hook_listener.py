import time
import shared_flags
from data.log_writer import log_entry
from queue import Queue

# Estos serán set por el main
command_queue = None
ctx = None
current_user = None
waiting_for_action = None

scan_buffer = ""
timestamps = []

def on_key(e):
    global scan_buffer, timestamps

    if e.event_type != "down":
        return

    now = time.time()
    timestamps.append(now)

    if len(timestamps) >= 2 and (now - timestamps[-2]) > 0.1:
        scan_buffer = ""
        timestamps = [now]
        return

    if len(e.name) == 1:
        scan_buffer += e.name

    if e.name == "enter":
        scan_time = timestamps[-1] - timestamps[0]
        code = scan_buffer.strip()
        scan_buffer = ""
        timestamps = []

        if scan_time < 0.3 and len(code) >= 3:
            print(f"🔍 Escaneo detectado: {code}")
            log_entry(f"📥 Escaneo encolado: {code}")
            command_queue.put(code)
        else:
            print("⌨ Entrada lenta ignorada")

