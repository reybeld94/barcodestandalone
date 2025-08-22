import re
from data.log_writer import log_entry
from utils.modals import show_error_modal
from actions.clockin_wo import hacer_clockin_workorder
from actions.clockout import hacer_clockout
import shared_flags
from logic.validation import (
    validar_pre_clockin,
    validar_post_clockin,
    validar_pre_clockout,
    validar_post_clockout,
)
from config import OPERATION_MAP
import time

# Estado actual
current_user = {"id": None}
waiting_for_action = {"active": False}


def esperar_validacion_post_clockin(user_code, wo_number, max_retries=10):
    for _ in range(max_retries):
        if validar_post_clockin(user_code, wo_number):
            return True
        time.sleep(2)
    return False

def esperar_validacion_post_clockout(user_code, wo_number, max_retries=10):
    for _ in range(max_retries):
        if validar_post_clockout(user_code, wo_number):
            return True
        time.sleep(2)
    return False

def on_key(event):
    if event.name == "enter":
        return
    if event.event_type != "down":
        return

    char = event.name
    if len(char) > 1 and not char.startswith("shift"):
        return

    handle_input(char)


scan_buffer = ""


def handle_input(char):
    global scan_buffer

    if char == "#":
        process_code(scan_buffer)
        scan_buffer = ""
    else:
        scan_buffer += char


def process_code(code, current_user, waiting_for_action, ctx):

    print(f"🔎 Código escaneado: {code}")

    # Escaneo de usuario
    if code.startswith("A#"):
        user_id = code[2:]
        current_user["id"] = user_id
        waiting_for_action["active"] = True
        log_entry(f"👤 Usuario escaneado: {user_id}", ctx)
        return True

    if not waiting_for_action["active"] or current_user["id"] is None:
        log_entry("⚠️ Escanee primero su ID de usuario.", ctx)
        show_error_modal("⚠️ PLEASE SCAN YOUR USER ID FIRST", duration=5, ctx=ctx)
        return False

    user_id = current_user["id"]

    # Formato universal: 3136O51R80
    import re
    if re.fullmatch(r"\d+O\d+R\d+", code):
        wo, op_router = code.split("O")
        op_id, router_id = op_router.split("R")

        op_name = OPERATION_MAP.get(op_id)
        if not op_name:
            log_entry(f"❌ Operación desconocida: {op_id}", ctx)
            show_error_modal("❌ UNKNOWN OPERATION ID", duration=5, ctx=ctx)
            return False

        # Si YA está clock in → Clock Out
        if validar_pre_clockin(user_id):
            if not validar_pre_clockout(user_id, wo):
                log_entry("⚠️ You are not clocked into this job", ctx)
                show_error_modal("⚠️ YOU ARE NOT CLOCKED INTO THIS JOB", duration=5, ctx=ctx)
                return True
            shared_flags.hook_enabled = False
            result = hacer_clockout(user_id, wo, ctx)
            if result.startswith("✅"):
                if esperar_validacion_post_clockout(user_id, wo):
                    log_entry(f"✅ Clock Out exitoso en WO {wo}", ctx)
                else:
                    log_entry(f"❌ Clock Out falló por validación post", ctx)
                    show_error_modal("❌ CLOCK OUT VALIDATION FAILED", duration=5, ctx=ctx)
            else:
                log_entry(f"❌ Clock Out falló: {result}", ctx)
                show_error_modal("❌ CLOCK OUT FAILED", duration=5, ctx=ctx)


        # Si NO está clock in → Clock In
        else:
            shared_flags.hook_enabled = False
            result = hacer_clockin_workorder(user_id, op_name, router_id, wo)
            if result.startswith("✅"):
                if esperar_validacion_post_clockin(user_id, wo):
                    log_entry(f"✅ Clock In exitoso en WO {wo}", ctx)
                else:
                    log_entry(f"❌ Clock In falló por validación post", ctx)
                    show_error_modal("❌ CLOCK IN VALIDATION FAILED", duration=5, ctx=ctx)
            else:
                log_entry(f"❌ Clock In falló: {result}", ctx)
                show_error_modal("❌ CLOCK IN FAILED", duration=5, ctx=ctx)

        # Limpiar estados
        current_user["id"] = None
        waiting_for_action["active"] = False
        shared_flags.hook_passive_mode = True
        return True

    # Si el código no es válido
    log_entry(f"❌ Código inválido: {code}", ctx)
    show_error_modal("❌ INVALID BARCODE FORMAT", duration=5, ctx=ctx)
    return False

