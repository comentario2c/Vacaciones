from app.auth.hashing import hashear_password
from app.db.db import get_connection

def crear_admin():
    email = "acontreras@ali.cl"
    password_plano = "0355"
    rol = "admin"

    conn = get_connection()
    cursor = conn.cursor()

    password_hashed = hashear_password(password_plano)

    cursor.execute("""
        INSERT INTO Usuario (Email, Rol, PasswordHash)
        VALUES (%s, %s, %s)
    """, (email, rol, password_hashed))

    conn.commit()
    cursor.close()
    conn.close()

    print("Usuario creado correctamente.")