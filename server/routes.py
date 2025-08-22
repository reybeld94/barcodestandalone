from flask import Blueprint, request, jsonify
from datetime import datetime

api_bp = Blueprint('api', __name__)

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

        from actions.clockin_wo import hacer_clockin_workorder

        result = hacer_clockin_workorder(
            data['user_id'],
            data['operation'],
            data['router_id'],
            data['wo_number']
        )

        success = result.startswith("✅")

        return jsonify({
            'success': success,
            'message': result,
            'timestamp': datetime.now().isoformat()
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

        from actions.clockout import hacer_clockout

        qty = data.get('qty', 1.0)

        result = hacer_clockout(
            data['user_id'],
            data['wo_number'],
            qty
        )

        success = result.startswith("✅")

        return jsonify({
            'success': success,
            'message': result,
            'timestamp': datetime.now().isoformat()
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
