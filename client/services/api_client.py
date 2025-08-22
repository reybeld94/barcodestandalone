import requests
import time
from datetime import datetime
from config import SERVER_URL, POLL_INTERVAL, COMMAND_TIMEOUT

class APIClient:
    def __init__(self):
        self.base_url = SERVER_URL
        
    def send_clockin_wo(self, user_id, wo_number, operation, router_id):
        """Enviar comando de clock in work order"""
        try:
            data = {
                'user_id': user_id,
                'wo_number': wo_number,
                'operation': operation,
                'router_id': router_id
            }
            
            response = requests.post(f"{self.base_url}/clockin-wo", json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result['success']:
                return result['command_id']
            else:
                raise Exception(result.get('error', 'Error desconocido'))
                
        except requests.RequestException as e:
            raise Exception(f"Error de conexión: {str(e)}")
        except Exception as e:
            raise Exception(f"Error enviando clockin: {str(e)}")
    
    def send_clockout(self, user_id, wo_number, qty=1.0):
        """Enviar comando de clock out"""
        try:
            data = {
                'user_id': user_id,
                'wo_number': wo_number,
                'qty': qty
            }
            
            response = requests.post(f"{self.base_url}/clockout", json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result['success']:
                return result['command_id']
            else:
                raise Exception(result.get('error', 'Error desconocido'))
                
        except requests.RequestException as e:
            raise Exception(f"Error de conexión: {str(e)}")
        except Exception as e:
            raise Exception(f"Error enviando clockout: {str(e)}")
    
    def get_command_status(self, command_id):
        """Obtener status de un comando"""
        try:
            response = requests.get(f"{self.base_url}/status/{command_id}", timeout=5)
            response.raise_for_status()
            
            result = response.json()
            if result['success']:
                return result['command']
            else:
                raise Exception(result.get('error', 'Error obteniendo status'))
                
        except requests.RequestException as e:
            raise Exception(f"Error de conexión: {str(e)}")
        except Exception as e:
            raise Exception(f"Error obteniendo status: {str(e)}")
    
    def wait_for_command_completion(self, command_id, timeout=COMMAND_TIMEOUT):
        """Esperar a que un comando se complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                command = self.get_command_status(command_id)
                status = command['status']
                
                if status == 'completed':
                    return True, command['message']
                elif status == 'failed':
                    return False, command['message']
                elif status in ['pending', 'processing']:
                    time.sleep(POLL_INTERVAL)
                    continue
                else:
                    return False, f"Estado desconocido: {status}"
                    
            except Exception as e:
                print(f"Error polling status: {e}")
                time.sleep(POLL_INTERVAL)
        
        return False, "Timeout esperando respuesta del servidor"
    
    def check_server_health(self):
        """Verificar que el servidor esté funcionando"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            
            result = response.json()
            return result['status'] == 'ok'
            
        except:
            return False

# Instancia global del cliente
api_client = APIClient()
