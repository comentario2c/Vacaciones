from fastapi import APIRouter, HTTPException
from app.crud.trabajadores.models import TrabajadorCrear
from app.crud.trabajadores.crud import crear_trabajador

router = APIRouter(prefix="/trabajadores", tags=["trabajadores"])

@router.post("/crear")
def registrar_trabajador(datos: TrabajadorCrear):
    try:
        crear_trabajador(datos)
        return {"msg": "Trabajador creado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))