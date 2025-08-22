import os

# Configuración del servidor
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Configuración de la base de datos MIE
DB_SERVER = 'GUNDMAIN'
DB_USER = 'mie'
DB_PASSWORD = 'mie'
DB_NAME = 'GunderlinLive'

# Timeouts
COMMAND_TIMEOUT = 30  # segundos
VALIDATION_TIMEOUT = 10  # segundos
