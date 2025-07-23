from pydantic import BaseModel
from datetime import date

class PermisosListar(BaseModel):
    ID_Permiso: int
    RutTrabajador: str
    NombreTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    ConCargoVacaciones: bool
    Motivo: str

class Permiso(BaseModel):
    ID_Permiso: int
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    ConCargoVacaciones: bool
    Motivo: str

class PermisoCrear(BaseModel):
    RutTrabajador: str
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    ConCargoVacaciones: bool
    Motivo: str

class PermisoActualizar(BaseModel):
    FechaInicio: date
    FechaFin: date
    DiasTomados: int
    ConCargoVacaciones: bool
    Motivo: str