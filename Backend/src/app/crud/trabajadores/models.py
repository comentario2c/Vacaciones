from pydantic import BaseModel, Field
from datetime import date

class TrabajadorCrear(BaseModel):
    RutTrabajador: str = Field(min_length=7, max_length=9)
    Nombre: str = Field(min_length=1, max_length=50)
    FechaContrato: date

class Trabajador(BaseModel):
    RutTrabajador: str
    Nombre: str
    FechaContrato: date

class TrabajadorActualizar(BaseModel):
    Nombre: str
    FechaContrato: date