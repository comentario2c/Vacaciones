from datetime import date
from app.db.db import get_connection
from app.services.vacaciones.configuracion.logica import obtener_configuracion_vacaciones
from app.services.vacaciones.configuracion.logica import obtener_configuracion_vacaciones
from app.services.vacaciones.dias_base.logica import obtener_dias_base
from app.services.vacaciones.progresivos.logica import obtener_dias_progresivos_totales

def obtener_dias_pendientes(RutTrabajador: str, anio_objetivo: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Obtener datos base
        cursor.execute("""
            SELECT FechaContrato, DiasPendientesBase
            FROM Trabajador
            WHERE RutTrabajador = %s AND Estado = true
        """, (RutTrabajador,))
        trabajador = cursor.fetchone()
        if not trabajador:
            raise ValueError(f"Trabajador {RutTrabajador} no encontrado o inactivo")

        # Cargar config una vez
        config = obtener_configuracion_vacaciones()
        
        fecha_contrato = trabajador["FechaContrato"]
        pendientes_base = int(trabajador["DiasPendientesBase"])
        anio_inicio = max(
            fecha_contrato.year + 1,
            config["anio_inicio_calculo_pendientes"]  # nuevo campo traído desde la tabla
        )
        anios_previos = range(anio_inicio, anio_objetivo)

        # Calcular días otorgados en años anteriores
        otorgados = 0
        for anio in anios_previos:
            otorgados += obtener_dias_base(RutTrabajador, anio)
            otorgados += obtener_dias_progresivos_totales(RutTrabajador, anio)

        # Calcular días usados hasta el 31 de diciembre del año anterior
        fecha_limite = date(anio_objetivo - 1, 12, 31)
        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM MovimientoVacaciones
            WHERE RutTrabajador = %s AND FechaInicio <= %s
        """, (RutTrabajador, fecha_limite))
        movimientos = cursor.fetchall()

        cursor.execute("""
            SELECT FechaInicio, FechaFin
            FROM Permisos
            WHERE RutTrabajador = %s AND FechaInicio <= %s AND ConCargoVacaciones = true
        """, (RutTrabajador, fecha_limite))
        permisos = cursor.fetchall()

        # Sumar días hábiles tomados
        from app.utils.dias_habiles import contar_dias_habiles  # asumirás que tienes esta función

        usados = 0
        for mov in movimientos + permisos:
            usados += contar_dias_habiles(mov["FechaInicio"], mov["FechaFin"])

        pendientes = max(0, otorgados + pendientes_base - usados)
        return pendientes

    finally:
        cursor.close()
        conn.close()