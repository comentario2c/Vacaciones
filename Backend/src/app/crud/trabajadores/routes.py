from fastapi import APIRouter, HTTPException

# Crear trabajador
from app.crud.trabajadores.models import TrabajadorCrear
from app.crud.trabajadores.crud import crear_trabajador

# Listar trabajadores
from app.crud.trabajadores.crud import obtener_trabajadores
from app.crud.trabajadores.models import Trabajador

# Actualizar trabajador
from app.crud.trabajadores.models import TrabajadorActualizar
from app.crud.trabajadores.crud import actualizar_trabajador

# Eliminar trabajador
from app.crud.trabajadores.crud import eliminar_trabajador

# Obtener trabajador por rut
from app.crud.trabajadores.crud import obtener_trabajador_por_rut

router = APIRouter()

@router.post("/crear")
def registrar_trabajador(datos: TrabajadorCrear):
    try:
        crear_trabajador(datos)
        return {"msg": "Trabajador creado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[Trabajador])
def listar_trabajadores():
    return obtener_trabajadores()

@router.put("/{rut}")
def editar_trabajador(rut: str, datos: TrabajadorActualizar):
    try:
        actualizar_trabajador(rut, datos)
        return {"msg": "Trabajador actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{rut}")
def eliminar_trabajador_route(rut: str):
    try:
        eliminar_trabajador(rut)
        return {"msg": "Trabajador eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{rut}", response_model=Trabajador)
def obtener_un_trabajador(rut: str):
    try:
        return obtener_trabajador_por_rut(rut)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
