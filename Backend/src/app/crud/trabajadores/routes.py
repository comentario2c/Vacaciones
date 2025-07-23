from fastapi import APIRouter, HTTPException
from app.crud.trabajadores.models import TrabajadorCrear, TrabajadorActualizar, Trabajador
from app.crud.trabajadores.crud import (
    crear_trabajador,
    obtener_trabajadores,
    obtener_trabajador_por_rut,
    actualizar_trabajador,
    eliminar_trabajador,
)
from typing import List

router = APIRouter()

@router.post("/crear", response_model=Trabajador, tags=["trabajadores"])
def crear(datos: TrabajadorCrear):
    try:
        crear_trabajador(datos)
        return obtener_trabajador_por_rut(datos.RutTrabajador)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/", response_model=List[Trabajador], tags=["trabajadores"])
def listar():
    return obtener_trabajadores()


@router.get("/{rut}", response_model=Trabajador, tags=["trabajadores"])
def obtener(rut: str):
    try:
        return obtener_trabajador_por_rut(rut)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.put("/{rut}", tags=["trabajadores"])
def editar(rut: str, datos: TrabajadorActualizar):
    try:
        actualizar_trabajador(rut, datos)
        return {"mensaje": "Trabajador actualizado"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.delete("/{rut}", tags=["trabajadores"])
def eliminar(rut: str):
    try:
        eliminar_trabajador(rut)
        return {"mensaje": "Trabajador marcado como inactivo"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
