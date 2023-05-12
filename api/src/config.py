from dotenv import load_dotenv
from secrets import token_hex
from os import environ, getcwd

load_dotenv()

SERVER_HOST = "localhost"
SERVER_PORT = 8000
FRONTEND_HOST = "localhost"
FRONTEND_PORT = 3000
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
BASE_DIR = getcwd()
DATABASE_URL = environ.get("DATABASE_URL")
SECRET_KEY = token_hex(30)
JWT_ALGORITHM = "HS256"
MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = "465"
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
