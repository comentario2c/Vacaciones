from app.db.db import get_connection
from app.crud.movimientoVacaciones.models import MovimientoVacaciones, MovimientoVacacionesCrear, MovimientoVacacionesActualizar, MovimientoVacacionesEditar
from mysql.connector import IntegrityError
from datetime import date, timedelta

def obtener_movimientos() -> list[MovimientoVacaciones]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ID_Movimiento, RutTrabajador, NombreTrabajador, FechaInicio, FechaFin, DiasTomados, Observaciones
        FROM VacacionesListar
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

def actualizar_movimiento(id_mov: int, datos: MovimientoVacacionesEditar):
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

def obtener_movimiento_por_id(id_mov: int) -> MovimientoVacacionesEditar:
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

    return MovimientoVacacionesEditar(**fila)

def calcular_dias_disponibles(rut: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar trabajador
    cursor.execute("""
        SELECT FechaContrato, SaldoVacaciones, AnosRestantes
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    trabajador = cursor.fetchone()

    if not trabajador:
        cursor.close()
        conn.close()
        raise ValueError("Trabajador no encontrado")

    saldo = trabajador["SaldoVacaciones"]
    años_restantes = trabajador["AnosRestantes"]
    año_ingreso = trabajador["FechaContrato"].year
    año_progresivo = año_ingreso + años_restantes

    # Calcular días progresivos
    dias_progresivos = 0
    if anio >= año_progresivo:
        dias_progresivos = 1 + ((anio - año_progresivo) // 3)

    # Calcular días ya tomados en ese año
    cursor.execute("""
        SELECT SUM(DiasTomados) as total
        FROM MovimientoVacaciones
        WHERE RutTrabajador = %s AND YEAR(FechaInicio) = %s
    """, (rut, anio))
    fila = cursor.fetchone()
    dias_usados = fila["total"] if fila["total"] else 0

    cursor.close()
    conn.close()

    dias_disponibles = max((saldo + dias_progresivos - dias_usados), 0)
    return dias_disponibles

def obtener_reporte_vacaciones(anio: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT T.RutTrabajador, T.Nombre, T.Cargo, M.FechaInicio, M.FechaFin
        FROM MovimientoVacaciones M
        JOIN Trabajador T ON M.RutTrabajador = T.RutTrabajador
        WHERE YEAR(M.FechaInicio) = %s OR YEAR(M.FechaFin) = %s
    """, (anio, anio))

    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    reporte = {}

    for r in registros:
        rut = r["RutTrabajador"]
        nombre = r["Nombre"]
        cargo = r["Cargo"]
        fecha_inicio = r["FechaInicio"]
        fecha_fin = r["FechaFin"]   

        # Asegurar que solo incluya días del año solicitado
        fecha_inicio = max(fecha_inicio, date(anio, 1, 1))
        fecha_fin = min(fecha_fin, date(anio, 12, 31))

        dias = []
        actual = fecha_inicio
        while actual <= fecha_fin:
            dias.append(actual.strftime("%Y-%m-%d"))
            actual += timedelta(days=1)

        if rut not in reporte:
            reporte[rut] = {"rut": rut, "nombre": nombre, "cargo": cargo, "dias": dias}
        else:
            reporte[rut]["dias"].extend(dias)

    # Eliminar duplicados en los días (por si hay más de un movimiento en el año)
    for item in reporte.values():
        item["dias"] = sorted(list(set(item["dias"])))

    return list(reporte.values())