from flask import Blueprint, request, jsonify
from datetime import datetime
from queue_handler import command_queue

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Servidor funcionando',
        'queue_running': command_queue.running
    })


@api_bp.route('/clockin-wo', methods=['POST'])
def clockin_wo():
    try:
        data = request.json

        required_fields = ['user_id', 'wo_number', 'operation', 'router_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400

        command_id = command_queue.add_command('clockin-wo', data)

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

        required_fields = ['user_id', 'wo_number']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400

        if 'qty' not in data:
            data['qty'] = 1.0

        command_id = command_queue.add_command('clockout', data)

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
    command = command_queue.get_command_status(command_id)

    if not command:
        return jsonify({
            'success': False,
            'error': 'Comando no encontrado'
        }), 404

    return jsonify({
        'success': True,
        'command': command
    })


@api_bp.route('/commands', methods=['GET'])
def list_commands():
    commands = command_queue.get_all_commands()
    return jsonify({
        'success': True,
        'commands': commands,
        'total': len(commands)
    })


@api_bp.route('/queue/status', methods=['GET'])
def queue_status():
    return jsonify({
        'success': True,
        'running': command_queue.running,
        'pending_commands': command_queue.queue.qsize(),
        'total_commands': len(command_queue.commands)
    })
