from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector
from app.auth.hashing import verificar_password
from app.auth.jwt_handler import crear_token
from app.db.db import get_connection
from app.auth.dependiences import requiere_rol

router = APIRouter()

class Credenciales(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(datos: Credenciales):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Email, Rol, PasswordHash FROM Usuario WHERE Email = %s", (datos.email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if not usuario or not verificar_password(datos.password, usuario['PasswordHash']):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        token = crear_token({
            "sub": usuario["Email"],
            "rol": usuario["Rol"]
        })

        return {"access_token": token, "token_type": "bearer"}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Error al conectarse a la base de datos")