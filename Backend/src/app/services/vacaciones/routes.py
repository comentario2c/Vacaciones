from fastapi import APIRouter, HTTPException
from app.db.db import get_connection
from app.services.vacaciones.progresivos.logica import calcular_dias_progresivos
from app.services.vacaciones.pendientes.logica import calcular_dias_pendientes
from app.services.vacaciones.pedidos.logica import calcular_dias_pedidos
from app.services.vacaciones.saldo.logica import calcular_saldo_vacaciones
from app.services.vacaciones.saldo_total.logica import calcular_saldo_total

router = APIRouter()

@router.get("/progresivos/{rut}/{anio}", response_model=int)
def obtener_dias_progresivos(rut: str, anio: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT FechaContrato, AnosRestantes
        FROM Trabajador
        WHERE RutTrabajador = %s
    """, (rut,))
    
    trabajador = cursor.fetchone()
    cursor.close()
    conn.close()

    if not trabajador:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")

    dias = calcular_dias_progresivos(trabajador["FechaContrato"], trabajador["AnosRestantes"], anio)
    return dias

@router.get("/pendientes/{rut}/{anio}", response_model=int)
def obtener_dias_pendientes(rut: str, anio: int):
    try:
        return calcular_dias_pendientes(rut, anio)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/pedidos/{rut}/{anio}", response_model=int)
def obtener_dias_pedidos(rut: str, anio: int):
    try:
        return calcular_dias_pedidos(rut, anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/saldo/{rut}/{anio}", response_model=int)
def obtener_saldo_vacaciones(rut: str, anio: int):
    try:
        return calcular_saldo_vacaciones(rut, anio)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/saldo-total/{rut}/{anio}", response_model=int)
def obtener_saldo_total(rut: str, anio: int):
    try:
        return calcular_saldo_total(rut, anio)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))