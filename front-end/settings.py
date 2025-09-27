from dotenv import load_dotenv
from os import environ
load_dotenv()

hostname = environ.get('BACKEND_HOSTNAME', 'localhost')
port = environ.get("BACKEND_PORT", 5000)
SECRET_KEY = environ['SECRET_KEY']
BACKEND_URL = f"http://{hostname}:{port}"
SERVER_PORT = environ.get('SERVER_PORT', 8000)