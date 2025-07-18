from fastapi import APIRouter, Depends, HTTPException
from app.db.db import get_connection
from services.feriados.sincronizar_feriados import sincronizar_feriados_chile

router = APIRouter()

@router.post("/feriados/sincronizar/{anio}", tags=["Feriados"])
def cargar_feriados_chile(anio: int):
    try:
        conn = get_connection()
        return sincronizar_feriados_chile(conn, anio)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))