from dotenv import load_dotenv
from secrets import token_hex
from os import environ, getcwd

load_dotenv()

SERVER_HOST = "192.168.0.10"
SERVER_PORT = 8000
BASE_DIR = getcwd()
DATABASE_URL = environ.get("DATABASE_URL")
SECRET_KEY = token_hex(30)
JWT_ALGORITHM = "HS256"
MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = "465"
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
