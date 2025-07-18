from app.services.vacaciones.dias_base.logica import obtener_dias_base
from app.services.vacaciones.progresivos.logica import obtener_dias_progresivos_totales

def obtener_total_disponible_en_anio(rut: str, anio: int) -> int:
    dias_base = obtener_dias_base(rut, anio)
    progresivos = obtener_dias_progresivos_totales(rut, anio)
    return dias_base + progresivos