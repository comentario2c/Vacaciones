from app.db.db import get_connection

def calcular_dias_pedidos(rut: str, anio: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT SUM(DiasTomados) AS total
        FROM Permisos
        WHERE RutTrabajador = %s AND Vacaciones = TRUE AND YEAR(FechaInicio) < %s
    """, (rut, anio))

    fila = cursor.fetchone()
    total = fila["total"] if fila["total"] else 0

    cursor.close()
    conn.close()
    return total