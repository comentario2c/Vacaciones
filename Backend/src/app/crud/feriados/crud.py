from mysql.connector import Error

def crear_feriado(conn, fecha, nombre):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM FeriadosNacionales WHERE fecha = %s", (fecha,))
        if cursor.fetchone()[0]:
            raise ValueError("Ya existe un feriado en esa fecha")

        cursor.execute("INSERT INTO FeriadosNacionales (fecha, nombre) VALUES (%s, %s)", (fecha, nombre))
        conn.commit()
        return {"mensaje": "Feriado creado"}

    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Error al crear feriado: {e}")
    finally:
        cursor.close()
        conn.close()


def editar_feriado(conn, ID_FeriadosNacionales, fecha, nombre):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE FeriadosNacionales SET fecha = %s, nombre = %s WHERE ID_FeriadosNacionales = %s", (fecha, nombre, ID_FeriadosNacionales))
        if cursor.rowcount == 0:
            raise ValueError("No se encontró el feriado a editar")
        conn.commit()
        return {"mensaje": "Feriado actualizado"}

    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Error al editar feriado: {e}")
    finally:
        cursor.close()
        conn.close()


def eliminar_feriado(conn, ID_FeriadosNacionales):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM FeriadosNacionales WHERE ID_FeriadosNacionales = %s", (ID_FeriadosNacionales,))
        if cursor.rowcount == 0:
            raise ValueError("No se encontró el feriado a eliminar")
        conn.commit()
        return {"mensaje": "Feriado eliminado"}

    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Error al eliminar feriado: {e}")
    finally:
        cursor.close()
        conn.close()

def obtener_feriados_por_anio(conn, anio: int):
    if anio < 1900 or anio > 2100:
        raise ValueError("El año debe estar entre 1900 y 2100")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ID_FeriadosNacionales, Fecha, Nombre 
            FROM FeriadosNacionales 
            WHERE YEAR(Fecha) = %s 
            ORDER BY Fecha ASC
        """, (anio,))
        feriados = cursor.fetchall()
        return feriados

    except Error as e:
        raise RuntimeError(f"Error al consultar feriados: {e}")

    finally:
        cursor.close()
        conn.close()