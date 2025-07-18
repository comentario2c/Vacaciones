from datetime import timedelta
from app.db.db import get_connection

def contar_dias_habiles(fecha_inicio, fecha_fin) -> int:
    if fecha_fin < fecha_inicio:
        return 0

    # Obtener feriados desde la BD
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Fecha FROM FeriadosNacionales
            WHERE Fecha BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        feriados = set(f[0] for f in cursor.fetchall())
    finally:
        cursor.close()
        conn.close()

    # Recorrer rango y contar hábiles
    total = 0
    dia_actual = fecha_inicio
    while dia_actual <= fecha_fin:
        if dia_actual.weekday() < 5 and dia_actual not in feriados:
            total += 1
        dia_actual += timedelta(days=1)

    return total