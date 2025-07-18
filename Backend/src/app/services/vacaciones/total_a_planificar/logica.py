from app.services.vacaciones.dias_base.logica import obtener_dias_base
from app.services.vacaciones.progresivos.logica import obtener_dias_progresivos_totales
from app.services.vacaciones.pendientes.logica import obtener_dias_pendientes
from app.services.vacaciones.tomados.logica import obtener_dias_tomados

def obtener_saldo_completo(RutTrabajador: str, anio: int) -> dict:
    dias_base = obtener_dias_base(RutTrabajador, anio)
    progresivos = obtener_dias_progresivos_totales(RutTrabajador, anio)
    total_disponible = dias_base + progresivos

    pendientes = obtener_dias_pendientes(RutTrabajador, anio)
    tomados = obtener_dias_tomados(RutTrabajador, anio)

    total_a_planificar = total_disponible + pendientes - tomados
    total_a_planificar = max(0, total_a_planificar)  # nunca valores negativos

    return {
        "rut": RutTrabajador,
        "anio": anio,
        "vacaciones_base": dias_base,
        "dias_progresivos": progresivos,
        "total_disponible": total_disponible,
        "dias_pendientes": pendientes,
        "dias_tomados": tomados,
        "total_a_planificar": total_a_planificar
    }