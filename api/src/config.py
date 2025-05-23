from os import environ
from secrets import token_hex

from dotenv import load_dotenv

load_dotenv()

OAUTH2_CLIENT_ID = environ.get("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = environ.get("OAUTH2_CLIENT_SECRET")
OAUTH2_AUTH_URL = environ.get("OAUTH2_AUTH_URL")
OAUTH2_TOKEN_URL = environ.get("OAUTH2_TOKEN_URL")
OAUTH2_CERTS_URL = environ.get("OAUTH2_CERTS_URL")

DATABASE_URL = environ.get("DATABASE_URL")
TEST_DATABASE_URL = environ.get("TEST_DATABASE_URL")

SECRET_KEY = token_hex(30)

JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXP = 60 * 10  # 10 min in seconds
JWT_REFRESH_TOKEN_EXP = 60 * 60 * 24 * 21  # 21 days in seconds

MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")

ADMIN_ID = int(environ.get("ADMIN_ID"))
