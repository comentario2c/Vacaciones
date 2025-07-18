from datetime import date
from app.db.db import get_connection
from app.utils.dias_habiles import contar_dias_habiles

def obtener_dias_tomados(RutTrabajador: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Validar trabajador activo
        cursor.execute("""
            SELECT 1 FROM Trabajador
            WHERE RutTrabajador = %s AND Estado = true
        """, (RutTrabajador,))
        if not cursor.fetchone():
            raise ValueError(f"Trabajador {RutTrabajador} no encontrado o inactivo")

        # Rango de fechas del año
        fecha_inicio_anio = date(anio, 1, 1)
        fecha_fin_anio = date(anio, 12, 31)

        # Obtener movimientos de vacaciones
        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM MovimientoVacaciones
            WHERE RutTrabajador = %s AND FechaInicio BETWEEN %s AND %s
        """, (RutTrabajador, fecha_inicio_anio, fecha_fin_anio))
        movimientos = cursor.fetchall()

        # Obtener permisos con cargo a vacaciones
        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM Permisos
            WHERE RutTrabajador = %s AND ConCargoVacaciones = true AND FechaInicio BETWEEN %s AND %s
        """, (RutTrabajador, fecha_inicio_anio, fecha_fin_anio))
        permisos = cursor.fetchall()

        # Sumar días hábiles tomados
        usados = 0
        for registro in movimientos + permisos:
            usados += contar_dias_habiles(registro["FechaInicio"], registro["FechaFin"])

        return usados

    finally:
        cursor.close()
        conn.close()