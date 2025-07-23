import os
from dotenv import load_dotenv

load_dotenv()  # carga .env

class Settings:
    # Base de datos
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = int(os.getenv("DB_PORT", 3306))
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME     = os.getenv("DB_NAME")
    SECRET_KEY  = os.getenv("SECRET_KEY")
    
    # Enviar correo
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    MAIL_STARTTLS=True
    MAIL_SSL_TLS=False
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED"),
    USE_CREDENTIALS = True
    VALIDATE_CERTS = False
    PERMISOS_DESTINATARIOS = os.getenv("PERMISOS_DESTINATARIOS","").split(",")

    if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY]):
        raise ValueError("Faltan variables de entorno")

settings = Settings()