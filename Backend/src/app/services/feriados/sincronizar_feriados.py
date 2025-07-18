import holidays
from mysql.connector import Error

def sincronizar_feriados_chile(conn, anio_inicial: int):
    if anio_inicial < 1900 or anio_inicial > 2100:
        raise ValueError("El año debe estar entre 1900 y 2100")

    nuevos = 0

    try:
        cursor = conn.cursor()

        for anio in range(anio_inicial, anio_inicial + 4):  # Año base + 3
            feriados_cl = holidays.country_holidays('CL', years=[anio])

            for fecha, nombre in feriados_cl.items():
                cursor.execute("SELECT COUNT(*) FROM FeriadosNacionales WHERE fecha = %s", (fecha,))
                existe = cursor.fetchone()[0]

                if not existe:
                    cursor.execute(
                        "INSERT INTO FeriadosNacionales (fecha, nombre) VALUES (%s, %s)", (fecha, nombre)
                    )
                    nuevos += 1

        conn.commit()
        return {
            "anio_base": anio_inicial,
            "anio_final": anio_inicial + 3,
            "nuevos_insertados": nuevos
        }

    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Error al sincronizar feriados: {e}")

    finally:
        cursor.close()
        conn.close()