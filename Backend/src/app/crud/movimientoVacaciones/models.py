from pydantic import BaseModel
from datetime import date

class MovimientoVacaciones(BaseModel):
    ID_Movimiento: int
    RutTrabajador: str
    NombreTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Observaciones: str | None = None

class MovimientoVacacionesCrear(BaseModel):
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Observaciones: str | None = None

class MovimientoVacacionesActualizar(BaseModel):
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Observaciones: str | None = None

class MovimientoVacacionesEditar(BaseModel):
    ID_Movimiento: int
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Observaciones: str | None = None