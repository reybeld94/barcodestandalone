import re
from data.log_writer import log_entry
from utils.modals import show_error_modal
from services.api_client import api_client
from config import OPERATION_MAP
import time

# Estado actual
current_user = {"id": None}
waiting_for_action = {"active": False}

def process_code(code, current_user, waiting_for_action, ctx):
    """Procesar código escaneado y enviar al servidor"""
    
    print(f"🔎 Código escaneado: {code}")
    log_entry(f"📥 Escaneo encolado: {code}")

    # Escaneo de usuario
    if code.startswith("A#"):
        user_id = code[2:]
        current_user["id"] = user_id
        waiting_for_action["active"] = True
        log_entry(f"👤 Usuario escaneado: {user_id}")
        return True

    if not waiting_for_action["active"] or current_user["id"] is None:
        log_entry("⚠️ Escanee primero su ID de usuario.")
        if ctx:
            show_error_modal("⚠️ PLEASE SCAN YOUR USER ID FIRST", duration=5, ctx=ctx)
        return False

    user_id = current_user["id"]

    # Verificar conectividad del servidor
    if not api_client.check_server_health():
        log_entry("❌ Servidor no disponible")
        if ctx:
            show_error_modal("❌ SERVER NOT AVAILABLE", duration=5, ctx=ctx)
        return False

    # Formato universal: 3136O51R80
    if re.fullmatch(r"\d+O\d+R\d+", code):
        wo, op_router = code.split("O")
        op_id, router_id = op_router.split("R")

        op_name = OPERATION_MAP.get(op_id)
        if not op_name:
            log_entry(f"❌ Operación desconocida: {op_id}")
            if ctx:
                show_error_modal("❌ UNKNOWN OPERATION ID", duration=5, ctx=ctx)
            return False

        try:
            # Determinar si es clock in o clock out
            # (Esta lógica necesitará validación del servidor también)
            
            # Por ahora, alternamos basado en si ya está activo
            # TODO: Implementar validación pre via API
            
            # Enviar comando al servidor
            command_id = api_client.send_clockin_wo(user_id, wo, op_name, router_id)
            log_entry(f"⏳ Comando enviado al servidor: {command_id}")
            
            # Esperar resultado
            success, message = api_client.wait_for_command_completion(command_id)
            
            if success:
                log_entry(f"✅ Clock In exitoso en WO {wo}")
            else:
                log_entry(f"❌ Clock In falló: {message}")
                if ctx:
                    show_error_modal("❌ CLOCK IN FAILED", duration=5, ctx=ctx)

        except Exception as e:
            log_entry(f"❌ Error de comunicación: {str(e)}")
            if ctx:
                show_error_modal("❌ COMMUNICATION ERROR", duration=5, ctx=ctx)

        # Limpiar estados
        current_user["id"] = None
        waiting_for_action["active"] = False
        return True

    # Si el código no es válido
    log_entry(f"❌ Código inválido: {code}")
    if ctx:
        show_error_modal("❌ INVALID BARCODE FORMAT", duration=5, ctx=ctx)
    return False
