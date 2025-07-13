from app.db.db import get_connection
from app.services.vacaciones.progresivos.logica import calcular_dias_progresivos
from app.services.vacaciones.pendientes.logica import calcular_dias_pendientes
from app.services.vacaciones.pedidos.logica import calcular_dias_pedidos

def calcular_saldo_vacaciones(rut: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT FechaContrato, AnosRestantes, SaldoVacaciones
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    trabajador = cursor.fetchone()
    if not trabajador:
        cursor.close()
        conn.close()
        raise ValueError("Trabajador no encontrado")

    saldo_base = trabajador["SaldoVacaciones"]
    progresivos = calcular_dias_progresivos(trabajador["FechaContrato"], trabajador["AnosRestantes"], anio)
    pendientes = calcular_dias_pendientes(rut, anio)
    pedidos = calcular_dias_pedidos(rut, anio)

    # Días usados como vacaciones reales ese año
    cursor.execute("""
        SELECT SUM(DiasTomados) AS total
        FROM MovimientoVacaciones
        WHERE RutTrabajador = %s AND YEAR(FechaInicio) = %s
    """, (rut, anio))
    fila = cursor.fetchone()
    usados = fila["total"] if fila["total"] else 0

    cursor.close()
    conn.close()

    saldo = (saldo_base + progresivos + pendientes) - (usados + pedidos)
    return max(saldo, 0)