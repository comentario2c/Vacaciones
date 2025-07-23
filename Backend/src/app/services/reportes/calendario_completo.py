from app.db.db import get_connection
from app.services.vacaciones.total_a_planificar.logica import obtener_saldo_completo

def obtener_saldos_completos_por_anio(anio: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT RutTrabajador
            FROM Trabajador
            WHERE Estado = true
        """)
        trabajadores = cursor.fetchall()

        resultados = []
        for trabajador in trabajadores:
            rut = trabajador["RutTrabajador"]
            try:
                saldo = obtener_saldo_completo(rut, anio)
                resultados.append(saldo)
            except Exception as e:
                print(f"Error al calcular saldo para {rut}: {e}")
                # Opcional: puedes agregar un flag de error o dejarlo fuera

        return resultados

    finally:
        cursor.close()
        conn.close()