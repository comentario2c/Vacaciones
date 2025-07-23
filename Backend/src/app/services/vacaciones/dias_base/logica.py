from datetime import date
from app.db.db import get_connection
from app.services.vacaciones.configuracion.logica import obtener_configuracion_vacaciones

def calcular_antiguedad_en_anios(fecha_inicio: date, fecha_referencia: date) -> int:
    return max(0, fecha_referencia.year - fecha_inicio.year - (
        (fecha_referencia.month, fecha_referencia.day) < (fecha_inicio.month, fecha_inicio.day)
    ))

def obtener_dias_base(RutTrabajador: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT FechaContrato
            FROM Trabajador
            WHERE RutTrabajador = %s AND Estado = true
        """, (RutTrabajador,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Trabajador {RutTrabajador} no encontrado o inactivo")

        fecha_contrato = row["FechaContrato"]
        config = obtener_configuracion_vacaciones()

        # Si el año de cálculo es menor al año de inicio del sistema, no calcular nada
        if anio < config["anio_inicio_calculo_pendientes"]:
            return 0

        # Validar que haya cumplido al menos 1 año antes del 1 de enero del año consultado
        fecha_corte = date(anio, 1, 1)
        antiguedad = calcular_antiguedad_en_anios(fecha_contrato, fecha_corte)

        if antiguedad < 1:
            return 0

        return config["dias_base_anuales"]

    finally:
        cursor.close()
        conn.close()