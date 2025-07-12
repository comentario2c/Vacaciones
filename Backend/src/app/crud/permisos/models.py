from pydantic import BaseModel
from datetime import date

class Permiso(BaseModel):
    ID_Permiso: int
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Vacaciones: bool
    Motivo: str

class PermisoCrear(BaseModel):
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Vacaciones: bool
    Motivo: str

class PermisoActualizar(BaseModel):
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    Vacaciones: bool
    Motivo: str