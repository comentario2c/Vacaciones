from datetime import date
from app.services.vacaciones.configuracion.logica import obtener_configuracion_vacaciones
from app.db.db import get_connection

def calcular_antiguedad_en_anios(fecha_inicio: date, fecha_referencia: date) -> int:
    return max(0, fecha_referencia.year - fecha_inicio.year - (
        (fecha_referencia.month, fecha_referencia.day) < (fecha_inicio.month, fecha_inicio.day)
    ))

def obtener_dias_progresivos_totales(RutTrabajador: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Obtener datos del trabajador
        cursor.execute("""
            SELECT FechaContrato, DiasProgresivosBase, AnosRestantes
            FROM Trabajador
            WHERE RutTrabajador = %s AND Estado = true
        """, (RutTrabajador,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Trabajador {RutTrabajador} no encontrado o inactivo")

        fecha_contrato = row["FechaContrato"]
        progresivos_base = int(row["DiasProgresivosBase"])
        anos_restantes = int(row["AnosRestantes"])

        # 2. Obtener configuración
        config = obtener_configuracion_vacaciones()
        periodo = config["periodo_entre_progresivos"]

        # 3. Antigüedad al 1 de enero del año objetivo
        referencia = date(anio, 1, 1)
        antiguedad = calcular_antiguedad_en_anios(fecha_contrato, referencia)

        # 4. Progresivos ganados dentro del sistema
        if antiguedad < anos_restantes:
            nuevos = 0
        else:
            años_extra = antiguedad - anos_restantes
            nuevos = años_extra // periodo

        return progresivos_base + nuevos

    finally:
        cursor.close()
        conn.close()