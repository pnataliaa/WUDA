from dotenv import load_dotenv
from os import environ
load_dotenv()

hostname = environ.get('HOSTNAME', 'localhost')
port = environ.get("PORT", 5000)
SECRET_KEY = environ['SECRET_KEY']
BACKEND_URL = f"http://{hostname}:{port}"