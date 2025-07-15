from .models import PermisosListar, PermisoCrear, PermisoActualizar, Permiso
from app.db.db import get_connection

def obtener_permisos() -> list[PermisosListar]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT ID_Permiso, RutTrabajador, NombreTrabajador, FechaInicio, FechaFin, DiasTomados, Vacaciones, Motivo FROM PermisosListar")
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [PermisosListar(**fila) for fila in resultados]

def crear_permiso(permiso: PermisoCrear):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO Permisos (RutTrabajador, FechaInicio, FechaFin, DiasTomados, Vacaciones, Motivo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        permiso.RutTrabajador,
        permiso.FechaInicio,
        permiso.FechaFin,
        permiso.DiasTomados,
        permiso.Vacaciones,
        permiso.Motivo
    )

    cursor.execute(query, valores)
    conn.commit()

    cursor.close()
    conn.close()

def actualizar_permiso(id_permiso: int, datos: PermisoActualizar):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE Permisos
        SET FechaInicio = %s,
            FechaFin = %s,
            DiasTomados = %s,
            Vacaciones = %s,
            Motivo = %s
        WHERE ID_Permiso = %s
    """
    valores = (
        datos.FechaInicio,
        datos.FechaFin,
        datos.DiasTomados,
        datos.Vacaciones,
        datos.Motivo,
        id_permiso
    )

    cursor.execute(query, valores)
    conn.commit()

    if cursor.rowcount == 0:
        raise ValueError("No se encontró el permiso para actualizar")

    cursor.close()
    conn.close()

def eliminar_permiso(id_permiso: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Permisos WHERE ID_Permiso = %s", (id_permiso,))
    conn.commit()

    if cursor.rowcount == 0:
        raise ValueError("No se encontró el permiso para eliminar")

    cursor.close()
    conn.close()

def obtener_permiso_por_id(id_permiso: int) -> Permiso:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT ID_Permiso, RutTrabajador, FechaInicio, FechaFin, DiasTomados, Vacaciones, Motivo FROM Permisos WHERE ID_Permiso = %s", (id_permiso,))
    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if not fila:
        raise ValueError("Permiso no encontrado")

    return Permiso(**fila)