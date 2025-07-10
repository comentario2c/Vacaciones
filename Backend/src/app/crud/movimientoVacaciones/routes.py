from fastapi import APIRouter
from app.crud.movimientoVacaciones.crud import obtener_movimientos, crear_movimiento, actualizar_movimiento, eliminar_movimiento, obtener_movimiento_por_id
from app.crud.movimientoVacaciones.models import MovimientoVacaciones, MovimientoVacacionesCrear, MovimientoVacacionesActualizar
from fastapi import HTTPException
import holidays
from datetime import datetime

router = APIRouter()

# Rutas estaticas

@router.get("/", response_model=list[MovimientoVacaciones])
def listar_movimientos():
    return obtener_movimientos()

@router.post("/crear")
def registrar_movimiento(datos: MovimientoVacacionesCrear):
    try:
        crear_movimiento(datos)
        return {"msg": "Movimiento de vacaciones registrado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/feriados", response_model=list[str])
def obtener_feriados():
    años = [datetime.now().year, datetime.now().year + 1]
    feriados = holidays.country_holidays("CL", years=años)
    return [fecha.strftime("%Y-%m-%d") for fecha in feriados.keys()]

# Rutas dinamicas

@router.put("/{id_mov}")
def editar_movimiento(id_mov: int, datos: MovimientoVacacionesActualizar):
    try:
        actualizar_movimiento(id_mov, datos)
        return {"msg": "Movimiento actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id_mov}")
def eliminar_movimiento_route(id_mov: int):
    try:
        eliminar_movimiento(id_mov)
        return {"msg": "Movimiento eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id_mov}", response_model=MovimientoVacaciones)
def obtener_movimiento(id_mov: int):
    try:
        return obtener_movimiento_por_id(id_mov)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))