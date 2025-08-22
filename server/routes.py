from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime

api_bp = Blueprint('api', __name__)

# Para almacenar comandos en memoria (después será una queue)
commands = {}

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Servidor funcionando'
    })

@api_bp.route('/clockin-wo', methods=['POST'])
def clockin_wo():
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['user_id', 'wo_number', 'operation', 'router_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Generar ID único para el comando
        command_id = str(uuid.uuid4())
        
        # Simular procesamiento (después será la queue)
        commands[command_id] = {
            'status': 'pending',
            'type': 'clockin-wo',
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'message': 'Comando en cola'
        }
        
        return jsonify({
            'success': True,
            'command_id': command_id,
            'message': 'Clock In encolado correctamente'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/clockout', methods=['POST'])
def clockout():
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['user_id', 'wo_number']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Generar ID único para el comando
        command_id = str(uuid.uuid4())
        
        # Simular procesamiento (después será la queue)
        commands[command_id] = {
            'status': 'pending',
            'type': 'clockout',
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'message': 'Comando en cola'
        }
        
        return jsonify({
            'success': True,
            'command_id': command_id,
            'message': 'Clock Out encolado correctamente'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/status/<command_id>', methods=['GET'])
def get_status(command_id):
    if command_id not in commands:
        return jsonify({
            'success': False,
            'error': 'Comando no encontrado'
        }), 404
    
    return jsonify({
        'success': True,
        'command': commands[command_id]
    })

@api_bp.route('/commands', methods=['GET'])
def list_commands():
    return jsonify({
        'success': True,
        'commands': list(commands.values())
    })
