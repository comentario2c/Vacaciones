from app.db.db import get_connection
from app.crud.movimientoVacaciones.models import MovimientoVacaciones, MovimientoVacacionesCrear, MovimientoVacacionesActualizar
from mysql.connector import IntegrityError

def obtener_movimientos() -> list[MovimientoVacaciones]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ID_Movimiento, RutTrabajador, FechaInicio, FechaFin, DiasTomados, Observaciones
        FROM MovimientoVacaciones
    """)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [MovimientoVacaciones(**fila) for fila in resultados]

def crear_movimiento(datos: MovimientoVacacionesCrear):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO MovimientoVacaciones 
            (RutTrabajador, FechaInicio, FechaFin, DiasTomados, Observaciones)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            datos.RutTrabajador,
            datos.FechaInicio,
            datos.FechaFin,
            datos.DiasTomados,
            datos.Observaciones
        ))
        conn.commit()
    except IntegrityError:
        raise ValueError("El trabajador no existe o los datos son inválidos")
    finally:
        cursor.close()
        conn.close()

def actualizar_movimiento(id_mov: int, datos: MovimientoVacacionesActualizar):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM MovimientoVacaciones WHERE ID_Movimiento = %s", (id_mov,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Movimiento no encontrado")

    try:
        cursor.execute("""
            UPDATE MovimientoVacaciones
            SET RutTrabajador = %s,
                FechaInicio = %s,
                FechaFin = %s,
                DiasTomados = %s,
                Observaciones = %s
            WHERE ID_Movimiento = %s
        """, (
            datos.RutTrabajador,
            datos.FechaInicio,
            datos.FechaFin,
            datos.DiasTomados,
            datos.Observaciones,
            id_mov
        ))
        conn.commit()
    except IntegrityError:
        raise ValueError("Error al actualizar el movimiento (verifica el RUT)")
    finally:
        cursor.close()
        conn.close()

def eliminar_movimiento(id_mov: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM MovimientoVacaciones WHERE ID_Movimiento = %s", (id_mov,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Movimiento no encontrado")

    try:
        cursor.execute("DELETE FROM MovimientoVacaciones WHERE ID_Movimiento = %s", (id_mov,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def obtener_movimiento_por_id(id_mov: int) -> MovimientoVacaciones:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ID_Movimiento, RutTrabajador, FechaInicio, FechaFin, DiasTomados, Observaciones
        FROM MovimientoVacaciones
        WHERE ID_Movimiento = %s
    """, (id_mov,))

    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("Movimiento no encontrado")

    return MovimientoVacaciones(**fila)