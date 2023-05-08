from dotenv import load_dotenv
from os import environ

load_dotenv()

DATABASE_URL = environ.get("DATABASE_URL")
ASYNC_DB_URL = environ.get("DATABASE_URL").replace(
    "postgresql://", "postgresql+asyncpg://"
)
MAIL_HOST = environ.get("MAIL_HOST")
MAIL_PORT = environ.get("MAIL_PORT")
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
