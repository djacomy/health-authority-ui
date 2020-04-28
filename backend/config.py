import os, logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss')
SECRET_KEY = JWT_SECRET_KEY
BASE_SERVER_PATH = os.environ.get("BASE_SERVER_PATH", 'http://127.0.0.1:5000/')
FRONT_URL = os.environ.get("FRONT_URL", 'http://127.0.0.1:8080/')

AUTHMACHINE_URL = os.environ['AUTHMACHINE_URL']
AUTHMACHINE_CLIENT_ID = os.environ['AUTHMACHINE_CLIENT_ID']
AUTHMACHINE_CLIENT_SECRET = os.environ['AUTHMACHINE_CLIENT_SECRET']
AUTHMACHINE_API_TOKEN = os.environ.get('AUTHMACHINE_API_TOKEN')
AUTHMACHINE_SCOPE = 'openid email profile'


FIXTURES_LIST = os.environ.get("FIXTURES_LIST", 'users.json,resources.json')

POSTGRES = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('POSTGRES_USER'),
    'db': os.getenv('POSTGRES_DB'),
    'pw': os.getenv('POSTGRES_PASSWORD'),
    'port': os.getenv('POSTGRES_PORT', 5432),
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)


