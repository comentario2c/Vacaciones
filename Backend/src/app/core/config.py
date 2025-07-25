import os
from dotenv import load_dotenv

load_dotenv()  # carga .env

class Settings:
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = int(os.getenv("DB_PORT", 3306))
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME     = os.getenv("DB_NAME")
    SECRET_KEY  = os.getenv("SECRET_KEY")

    if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY]):
        raise ValueError("Faltan variables de entorno")

settings = Settings()