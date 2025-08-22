import time
import pyautogui

def esperar_y_localizar(imagen, timeout=10, confidence=0.6):
    """
    Espera hasta `timeout` segundos intentando localizar una imagen en pantalla.
    Retorna el centro de la imagen si se encuentra, o None si no.
    """
    print(f"⏳ Esperando {imagen}...")
    inicio = time.time()
    while time.time() - inicio < timeout:
        ubicacion = pyautogui.locateCenterOnScreen(imagen, confidence=confidence)
        if ubicacion:
            print(f"✅ {imagen} encontrada")
            return ubicacion
        time.sleep(0.5)
    print(f"❌ {imagen} no encontrada después de {timeout} segundos")
    return None
