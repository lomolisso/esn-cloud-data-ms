import os
from dotenv import load_dotenv

# Retrieve enviroment variables from .env file
load_dotenv()

SECRET_KEY: str = os.environ.get("SECRET_KEY")
DATA_MICROSERVICE_HOST: str = os.environ.get("DATA_MICROSERVICE_HOST")
DATA_MICROSERVICE_PORT: int = int(os.environ.get("DATA_MICROSERVICE_PORT"))

DATABASE_USER: str = os.environ.get("DATABASE_USER")
DATABASE_PASS: str = os.environ.get("DATABASE_PASS")
DATABASE_HOST: str = os.environ.get("DATABASE_HOST")
DATABASE_PORT: str = os.environ.get("DATABASE_PORT")
DATABASE_NAME: str = os.environ.get("DATABASE_NAME")

CLOUD_API_URL: str = os.environ.get("CLOUD_API_URL")

TIMEZONE: str = os.environ.get("TIMEZONE", "Chile/Continental")

ORIGINS: list = [
    "*"
]
