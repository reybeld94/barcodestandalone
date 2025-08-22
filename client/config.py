# Configuración del cliente
SERVER_URL = "http://localhost:5000/api"
POLL_INTERVAL = 1.0  # segundos para polling de status
COMMAND_TIMEOUT = 30  # segundos máximo para esperar comando
SCANNER_DETECTION_SPEED = 0.3  # velocidad máxima para detectar scanner

# Rutas y configuración general
LOGO_PATH = "images/logo.png"
TIMEOUT_SECONDS = 120
KIOSK_EXE_NAME = "Mie.Kiosk.exe"
KIOSK_SHORTCUT = "Mie.Kiosk.lnk"

# Mapeo de operaciones (migrado desde config.py original)
OPERATION_MAP = {
    "51": "OP Laser Cutting",
    "52": "OP Forming", 
    "53": "OP Welding",
    "54": "OP QC",
    "55": "OP Painting"
}

# UI Configuration
FONT_CODE = ("Consolas", 16)
MODAL_BG = "#ffeeee"
