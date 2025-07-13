from app.db.db import get_connection
from app.services.vacaciones.progresivos.logica import calcular_dias_progresivos

def calcular_saldo_total(rut: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT FechaContrato, AnosRestantes, SaldoVacaciones
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    trabajador = cursor.fetchone()
    cursor.close()
    conn.close()

    if not trabajador:
        raise ValueError("Trabajador no encontrado")

    progresivos = calcular_dias_progresivos(trabajador["FechaContrato"], trabajador["AnosRestantes"], anio)
    total = trabajador["SaldoVacaciones"] + progresivos
    return total