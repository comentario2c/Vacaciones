from fastapi import APIRouter
from app.services.vacaciones.total_a_planificar.logica import obtener_saldo_completo

router = APIRouter()

@router.get("/saldo-completo/{rut}/{anio}")
def get_saldo_completo(rut: str, anio: int):
    return obtener_saldo_completo(rut, anio)