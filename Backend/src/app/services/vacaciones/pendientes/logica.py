from datetime import datetime
from app.db.db import get_connection

def calcular_dias_pendientes(rut: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener fecha de contrato y saldo base
    cursor.execute("""
        SELECT FechaContrato, SaldoVacaciones
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    trabajador = cursor.fetchone()

    if not trabajador:
        cursor.close()
        conn.close()
        raise ValueError("Trabajador no encontrado")

    fecha_contrato = trabajador["FechaContrato"]
    saldo = trabajador["SaldoVacaciones"]

    año_inicio = fecha_contrato.year

    # Sumar todos los días tomados en años anteriores al de consulta
    cursor.execute("""
        SELECT SUM(DiasTomados) AS total
        FROM MovimientoVacaciones
        WHERE RutTrabajador = %s AND YEAR(FechaInicio) < %s
    """, (rut, anio))
    fila = cursor.fetchone()
    dias_usados = fila["total"] if fila["total"] else 0

    años_completos = max(anio - año_inicio, 0)
    dias_generados = saldo * años_completos

    pendientes = max(dias_generados - dias_usados, 0)

    cursor.close()
    conn.close()
    return pendientes