from fastapi import APIRouter, HTTPException
from app.db.db import get_connection
from app.crud.feriados.crud import crear_feriado, editar_feriado, eliminar_feriado, obtener_feriados_por_anio
from app.crud.feriados.models import FeriadoCreate, FeriadoUpdate, FeriadoOut
from typing import List

router = APIRouter()

@router.post("/feriados/crear", tags=["feriados"])
def crear(feriado: FeriadoCreate):
    try:
        conn = get_connection()
        return crear_feriado(conn, feriado.fecha, feriado.nombre)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feriados/{anio}", tags=["feriados"], response_model=List[FeriadoOut])
def listar(anio: int):
    try:
        conn = get_connection()
        return obtener_feriados_por_anio(conn, anio)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/feriados/{ID_FeriadosNacionales}", tags=["feriados"])
def editar(ID_FeriadosNacionales: int, feriado: FeriadoUpdate):
    try:
        conn = get_connection()
        return editar_feriado(conn, ID_FeriadosNacionales, feriado.fecha, feriado.nombre)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/feriados/{ID_FeriadosNacionales}", tags=["feriados"])
def eliminar(ID_FeriadosNacionales: int):
    try:
        conn = get_connection()
        return eliminar_feriado(conn, ID_FeriadosNacionales)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))