from pydantic import BaseModel, Field
from datetime import date

class TrabajadorCrear(BaseModel):
    RutTrabajador: str = Field(min_length=7, max_length=9)
    Nombre: str = Field(min_length=1, max_length=50)
    Cargo: str = Field(min_length=1, max_length=50)
    FechaContrato: date
    AnosRestantes: int
    SaldoVacaciones: int
    Estado: bool

class Trabajador(BaseModel):
    RutTrabajador: str
    Nombre: str
    Cargo: str
    FechaContrato: date
    AnosRestantes: int
    SaldoVacaciones: int

class TrabajadorActualizar(BaseModel):
    Nombre: str
    Cargo: str
    FechaContrato: date
    AnosRestantes: int
    SaldoVacaciones: int