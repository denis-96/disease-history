from os import environ, getcwd
from secrets import token_hex

from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = "localhost"
SERVER_PORT = 8000
FRONTEND_HOST = "localhost"
FRONTEND_PORT = 3000

OAUTH2_CLIENT_ID = environ.get("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = environ.get("OAUTH2_CLIENT_SECRET")
OAUTH2_AUTH_URL = environ.get("OAUTH2_AUTH_URL")
OAUTH2_TOKEN_URL = environ.get("OAUTH2_TOKEN_URL")
OAUTH2_CERTS_URL = environ.get("OAUTH2_CERTS_URL")


BASE_DIR = getcwd()
DATABASE_URL = environ.get("DATABASE_URL")
SECRET_KEY = token_hex(30)
JWT_ALGORITHM = "HS256"
MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = "465"
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
ADMIN_ID = int(environ.get("ADMIN_ID"))
