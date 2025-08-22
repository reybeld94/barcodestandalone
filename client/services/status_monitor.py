import threading
import time
from services.api_client import api_client
from data.log_writer import log_entry

class StatusMonitor:
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.pending_commands = {}  # command_id -> callback
        
    def start_monitoring(self):
        """Iniciar monitoreo de comandos"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("🟢 Status monitor iniciado")
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            print("🔴 Status monitor detenido")
    
    def add_command_to_monitor(self, command_id, callback=None):
        """Agregar comando para monitorear"""
        self.pending_commands[command_id] = callback
        
    def _monitor_loop(self):
        """Loop principal de monitoreo"""
        while self.monitoring:
            try:
                # Revisar comandos pendientes
                completed_commands = []
                
                for command_id, callback in self.pending_commands.items():
                    try:
                        command = api_client.get_command_status(command_id)
                        status = command['status']
                        
                        if status in ['completed', 'failed']:
                            # Comando terminado
                            if callback:
                                callback(command_id, command)
                            completed_commands.append(command_id)
                            
                    except Exception as e:
                        print(f"Error monitoreando {command_id}: {e}")
                
                # Remover comandos completados
                for cmd_id in completed_commands:
                    del self.pending_commands[cmd_id]
                
                time.sleep(1)  # Polling cada segundo
                
            except Exception as e:
                print(f"Error en monitor loop: {e}")
                time.sleep(5)

# Instancia global
status_monitor = StatusMonitor()
