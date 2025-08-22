import threading
import time
import uuid
from datetime import datetime
from queue import Queue
from actions.clockin_wo import hacer_clockin_workorder
from actions.clockout import hacer_clockout
from logic.validation import (
    validar_pre_clockin, validar_post_clockin,
    validar_pre_clockout, validar_post_clockout
)


class CommandQueue:
    def __init__(self):
        self.queue = Queue()
        self.commands = {}
        self.worker_thread = None
        self.running = False

    def start(self):
        """Iniciar el worker thread"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.worker_thread.start()
            print("🟢 Queue handler iniciado")

    def stop(self):
        """Detener el worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
            print("🔴 Queue handler detenido")

    def add_command(self, command_type, data):
        """Agregar comando a la cola"""
        command_id = str(uuid.uuid4())
        command = {
            'id': command_id,
            'type': command_type,
            'data': data,
            'status': 'pending',
            'message': 'Comando en cola',
            'timestamp': datetime.now().isoformat(),
            'result': None,
        }
        self.commands[command_id] = command
        self.queue.put(command)
        print(f"📥 Comando {command_type} encolado: {command_id}")
        return command_id

    def get_command_status(self, command_id):
        """Obtener estado de un comando"""
        return self.commands.get(command_id)

    def get_all_commands(self):
        """Obtener todos los comandos"""
        return list(self.commands.values())

    def _worker(self):
        """Worker thread que procesa comandos"""
        while self.running:
            try:
                command = self.queue.get(timeout=1)
                self._process_command(command)
                self.queue.task_done()
            except Exception as e:
                if self.running:
                    print(f"❌ Error en worker: {e}")
                time.sleep(0.1)

    def _process_command(self, command):
        """Procesar un comando individual"""
        command_id = command['id']
        command_type = command['type']
        data = command['data']
        try:
            self._update_command(command_id, 'processing', 'Ejecutando comando...')
            print(f"⚙️ Procesando {command_type}: {command_id}")

            if command_type == 'clockin-wo':
                result = self._process_clockin_wo(data)
            elif command_type == 'clockout':
                result = self._process_clockout(data)
            else:
                result = f"❌ Tipo de comando desconocido: {command_type}"

            success = result.startswith("✅")
            status = 'completed' if success else 'failed'
            self._update_command(command_id, status, result)
            print(f"{'✅' if success else '❌'} Comando {command_id}: {result}")
        except Exception as e:
            error_msg = f"❌ Error ejecutando comando: {str(e)}"
            self._update_command(command_id, 'failed', error_msg)
            print(f"❌ Error en comando {command_id}: {e}")

    def _process_clockin_wo(self, data):
        """Procesar comando de clock in work order"""
        user_id = data['user_id']
        wo_number = data['wo_number']
        operation = data['operation']
        router_id = data['router_id']

        if validar_pre_clockin(user_id):
            return "⚠️ Usuario ya tiene un clock in activo"
        result = hacer_clockin_workorder(user_id, operation, router_id, wo_number)
        if result.startswith("✅"):
            time.sleep(2)
            if validar_post_clockin(user_id, wo_number):
                return f"✅ Clock In exitoso en WO {wo_number}"
            return "❌ Clock In falló en validación post"
        return result

    def _process_clockout(self, data):
        """Procesar comando de clock out"""
        user_id = data['user_id']
        wo_number = data['wo_number']
        qty = data.get('qty', 1.0)

        if not validar_pre_clockout(user_id, wo_number):
            return "⚠️ Usuario no está clock in en este WO"
        result = hacer_clockout(user_id, wo_number, qty)
        if result.startswith("✅"):
            time.sleep(2)
            if validar_post_clockout(user_id, wo_number):
                return f"✅ Clock Out exitoso en WO {wo_number}"
            return "❌ Clock Out falló en validación post"
        return result

    def _update_command(self, command_id, status, message):
        """Actualizar estado de un comando"""
        if command_id in self.commands:
            self.commands[command_id].update({
                'status': status,
                'message': message,
                'timestamp': datetime.now().isoformat(),
            })


command_queue = CommandQueue()
