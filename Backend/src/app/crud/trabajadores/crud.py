from app.db.db import get_connection
from mysql.connector import IntegrityError, Error
from app.crud.trabajadores.models import TrabajadorCrear, Trabajador, TrabajadorActualizar

def crear_trabajador(datos: TrabajadorCrear):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Trabajador (
                RutTrabajador, Nombre, Cargo, FechaContrato, AnosRestantes, DiasProgresivosBase, DiasPendientesBase, Estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datos.RutTrabajador,
            datos.Nombre,
            datos.Cargo,
            datos.FechaContrato,
            datos.AnosRestantes,
            datos.DiasProgresivosBase,
            datos.DiasPendientesBase,
            datos.Estado,
        ))
        conn.commit()
    except IntegrityError:
        raise ValueError("Ya existe un trabajador con ese RUT")
    finally:
        cursor.close()
        conn.close()

def obtener_trabajadores() -> list[Trabajador]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT RutTrabajador, Nombre, Cargo, FechaContrato, AnosRestantes, DiasProgresivosBase, DiasPendientesBase, Estado
        FROM Trabajador
        WHERE Estado = TRUE
    """)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Trabajador(**fila) for fila in resultados]

def obtener_trabajador_por_rut(rut: str) -> Trabajador:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT RutTrabajador, Nombre, Cargo, FechaContrato, AnosRestantes, DiasProgresivosBase, DiasPendientesBase, Estado
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    
    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("Trabajador no encontrado")

    return Trabajador(**fila)

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
            SET Nombre = %s,
                Cargo = %s,
                FechaContrato = %s,
                AnosRestantes = %s,
                DiasProgresivosBase = %s,
                DiasPendientesBase = %s
            WHERE RutTrabajador = %s
        """, (
            datos.Nombre,
            datos.Cargo,
            datos.FechaContrato,
            datos.AnosRestantes,
            datos.DiasProgresivosBase,
            datos.DiasPendientesBase,
            rut
        ))
        conn.commit()
    except Error:
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
        cursor.execute("UPDATE Trabajador SET Estado = FALSE WHERE RutTrabajador = %s", (rut,))
        conn.commit()
    except Error:
        raise ValueError("Error al marcar como inactivo al trabajador")
    finally:
        cursor.close()
        conn.close()