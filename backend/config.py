import os, logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))

SECRET_KEY = os.getenv('SECRET_KEY', 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')
FRONT_URL = os.environ.get("FRONT_URL", 'http://127.0.0.1:8080/')

AUTHMACHINE_URL = os.environ['AUTHMACHINE_URL']
AUTHMACHINE_CLIENT_ID = os.environ['AUTHMACHINE_CLIENT_ID']
AUTHMACHINE_CLIENT_SECRET = os.environ['AUTHMACHINE_CLIENT_SECRET']
AUTHMACHINE_API_TOKEN = os.environ.get('AUTHMACHINE_API_TOKEN')
AUTHMACHINE_SCOPE = 'openid email profile'


logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)


