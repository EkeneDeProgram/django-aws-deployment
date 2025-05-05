# Standard library imports
import os

# Related third-party imports
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Database settings
DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_HOST = os.getenv("DB_HOST")
DATABASE_PORT = int(os.getenv("DB_PORT", 5432))  # Cast to int for port

# Celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

# Secret key and debug flag
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True").lower() in (
    "true",
    "1",
    "yes",
)  # Convert env var to boolean
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(
    ","
)  # Split comma-separated hosts
