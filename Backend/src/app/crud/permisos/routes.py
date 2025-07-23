from fastapi import APIRouter, HTTPException, BackgroundTasks
from .crud import obtener_permisos, crear_permiso, actualizar_permiso, eliminar_permiso, obtener_permiso_por_id
from .models import PermisosListar, PermisoCrear, PermisoActualizar, Permiso
from app.utils.email import enviar_correo_permiso, obtener_detalle_ultimo_permiso
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=list[PermisosListar])
def listar_permisos():
    return obtener_permisos()

@router.post("/crear")
async def registrar_permiso(datos: PermisoCrear, bg: BackgroundTasks):
    try:
        crear_permiso(datos)

        # Recuperar datos desde la vista PermisosListar
        detalle = obtener_detalle_ultimo_permiso(datos.RutTrabajador, datos.FechaInicio)
        nombre = detalle["NombreTrabajador"]
        con_cargo = detalle["ConCargoVacaciones"]
        con_cargo_str = "Sí" if con_cargo else "No"

        fechas = f"{datos.FechaInicio} a {datos.FechaFin}"
        motivo = datos.Motivo
        destinatario = settings.PERMISOS_DESTINATARIOS

        bg.add_task(enviar_correo_permiso, destinatario, nombre, fechas, motivo, con_cargo_str)

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