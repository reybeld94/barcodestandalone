from flask import Flask
from flask_cors import CORS
from routes import api_bp
import config

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    print(f"🟢 Servidor iniciando en puerto {config.PORT}")
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
