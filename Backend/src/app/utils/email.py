from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from typing import Union, List
from jinja2 import Environment, FileSystemLoader
from app.db.db import get_connection
import os

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    SUPPRESS_SEND=not settings.EMAIL_ENABLED,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

TEMPLATES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "templates", "email")
)

env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))

async def enviar_correo_permiso(destinatarios, nombre: str, fechas: str, motivo: str, con_cargo: str):
    plantilla = env.get_template("permiso_notificacion.html")
    html_renderizado = plantilla.render(
        trabajador=nombre,
        fechas=fechas,
        motivo=motivo,
        con_cargo=con_cargo
    )

    mensaje = MessageSchema(
        subject="📌 Permiso registrado",
        recipients=destinatarios,
        body=html_renderizado,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(mensaje)

def obtener_detalle_ultimo_permiso(rut: str, fecha_inicio) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT NombreTrabajador, ConCargoVacaciones
        FROM PermisosListar
        WHERE RutTrabajador = %s AND FechaInicio = %s
        ORDER BY ID_Permiso DESC
        LIMIT 1
    """, (rut, fecha_inicio))

    fila = cursor.fetchone()
    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("No se encontró el permiso recién creado")

    return fila