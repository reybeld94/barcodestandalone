# === Configuración general de la app local ===

# Ruta a las imágenes de UI si las necesitas (solo si usas modales visuales)
LOGO_PATH = "images/logo.png"

# Tiempo máximo de espera para acciones (si aplicas algún watchdog interno en el futuro)
TIMEOUT_SECONDS = 120

# Nombre del proceso ejecutable de Mie.Kiosk
KIOSK_EXE_NAME = "Mie.Kiosk.exe"
KIOSK_SHORTCUT = "Mie.Kiosk.lnk"

# Colores (si decides usar modales de error en el futuro)
MODAL_BG = "#ffeeee"

# Fuentes (solo si integras alguna GUI visual o modal tkinter)
FONT_CODE = ("Consolas", 16)

# Mapeo de operaciones válidas por ID del código de barras
OPERATION_MAP = {
    "51": "OP Laser Cutting",
    "52": "OP Forming",
    "53": "OP Welding",
    "54": "OP QC",
    "55": "OP Painting"
}
