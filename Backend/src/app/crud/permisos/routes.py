from fastapi import APIRouter, HTTPException
from .crud import obtener_permisos, crear_permiso, actualizar_permiso, eliminar_permiso, obtener_permiso_por_id
from .models import Permiso, PermisoCrear, PermisoActualizar

router = APIRouter()

@router.get("/", response_model=list[Permiso])
def listar_permisos():
    return obtener_permisos()

@router.post("/crear")
def registrar_permiso(datos: PermisoCrear):
    try:
        crear_permiso(datos)
        return {"msg": "Permiso registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo registrar el permiso: {str(e)}")

@router.put("/{id_permiso}")
def editar_permiso(id_permiso: int, datos: PermisoActualizar):
    try:
        actualizar_permiso(id_permiso, datos)
        return {"msg": "Permiso actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id_permiso}")
def eliminar_permiso_route(id_permiso: int):
    try:
        eliminar_permiso(id_permiso)
        return {"msg": "Permiso eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{id_permiso}", response_model=Permiso)
def obtener_permiso(id_permiso: int):
    try:
        return obtener_permiso_por_id(id_permiso)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))