from fastapi import APIRouter
from app.services.reportes.calendario_completo import obtener_saldos_completos_por_anio

router = APIRouter()

@router.get("/saldos-completos/{anio}")
def get_saldos_completos_por_anio(anio: int):
    return obtener_saldos_completos_por_anio(anio)