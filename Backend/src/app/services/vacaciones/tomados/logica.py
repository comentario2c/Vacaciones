from datetime import date
from app.db.db import get_connection
from app.utils.dias_habiles import contar_dias_habiles
from app.services.vacaciones.configuracion.logica import obtener_configuracion_vacaciones

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

        # Obtener configuración
        config = obtener_configuracion_vacaciones()
        fecha_inicio_valida = date(config["anio_inicio_calculo_pendientes"], 1, 1)

        # Rango de fechas del año consultado
        fecha_inicio_anio = date(anio, 1, 1)
        fecha_fin_anio = date(anio, 12, 31)

        # Proteger si el año objetivo es anterior al inicio del sistema
        if fecha_fin_anio < fecha_inicio_valida:
            return 0

        # Usar el mayor entre el inicio del año y el inicio válido del sistema
        fecha_inicio_filtrada = max(fecha_inicio_anio, fecha_inicio_valida)

        # Obtener movimientos de vacaciones
        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM MovimientoVacaciones
            WHERE RutTrabajador = %s AND FechaInicio BETWEEN %s AND %s
        """, (RutTrabajador, fecha_inicio_filtrada, fecha_fin_anio))
        movimientos = cursor.fetchall()

        # Obtener permisos con cargo a vacaciones
        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM Permisos
            WHERE RutTrabajador = %s AND ConCargoVacaciones = true AND FechaInicio BETWEEN %s AND %s
        """, (RutTrabajador, fecha_inicio_filtrada, fecha_fin_anio))
        permisos = cursor.fetchall()

        # Sumar días hábiles tomados
        usados = 0
        for registro in movimientos + permisos:
            usados += contar_dias_habiles(registro["FechaInicio"], registro["FechaFin"])

        return usados

    finally:
        cursor.close()
        conn.close()