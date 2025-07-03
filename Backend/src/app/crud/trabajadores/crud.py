from app.db.db import get_connection
from mysql.connector import IntegrityError
from app.crud.trabajadores.models import TrabajadorCrear
from app.crud.trabajadores.models import Trabajador
from app.crud.trabajadores.models import TrabajadorActualizar
from mysql.connector import Error

def crear_trabajador(datos: TrabajadorCrear):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Trabajador (RutTrabajador, Nombre, Cargo, FechaContrato)
            VALUES (%s, %s, %s, %s)
        """, (datos.RutTrabajador, datos.Nombre, datos.Cargo, datos.FechaContrato))
        conn.commit()
    except IntegrityError as e:
        raise ValueError("Ya existe un trabajador con ese RUT")
    finally:
        cursor.close()
        conn.close()

def obtener_trabajadores() -> list[Trabajador]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT RutTrabajador, Nombre, Cargo, FechaContrato FROM Trabajador")
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Trabajador(**fila) for fila in resultados]

def actualizar_trabajador(rut: str, datos: TrabajadorActualizar):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM Trabajador WHERE RutTrabajador = %s", (rut,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Trabajador no encontrado")

    try:
        cursor.execute("""
            UPDATE Trabajador
            SET Nombre = %s, Cargo = %s, FechaContrato = %s
            WHERE RutTrabajador = %s
        """, (datos.Nombre, datos.Cargo, datos.FechaContrato, rut))
        conn.commit()
    except Error as e:
        raise ValueError("Error al actualizar trabajador")
    finally:
        cursor.close()
        conn.close()

def eliminar_trabajador(rut: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM Trabajador WHERE RutTrabajador = %s", (rut,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Trabajador no encontrado")

    try:
        cursor.execute("DELETE FROM Trabajador WHERE RutTrabajador = %s", (rut,))
        conn.commit()
    except Error:
        raise ValueError("Error al eliminar trabajador")
    finally:
        cursor.close()
        conn.close()

def obtener_trabajador_por_rut(rut: str) -> Trabajador:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT RutTrabajador, Nombre, Cargo, FechaContrato
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    
    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("Trabajador no encontrado")

    return Trabajador(**fila)