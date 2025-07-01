from app.db.db import get_connection
from mysql.connector import IntegrityError
from app.crud.trabajadores.models import TrabajadorCrear

def crear_trabajador(datos: TrabajadorCrear):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Trabajador (RutTrabajador, Nombre, FechaContrato)
            VALUES (%s, %s, %s)
        """, (datos.RutTrabajador, datos.Nombre, datos.FechaContrato))
        conn.commit()
    except IntegrityError as e:
        raise ValueError("Ya existe un trabajador con ese RUT")
    finally:
        cursor.close()
        conn.close()