from flask import Flask
from flask_cors import CORS
from routes import api_bp
from queue_handler import command_queue
import config
import atexit

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Función para cleanup al cerrar
def cleanup():
    print("🛑 Cerrando servidor...")
    command_queue.stop()

# Registrar cleanup
atexit.register(cleanup)

if __name__ == '__main__':
    print(f"🟢 Servidor iniciando en puerto {config.PORT}")

    # Iniciar queue handler
    command_queue.start()

    try:
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrumpido")
    finally:
        cleanup()
