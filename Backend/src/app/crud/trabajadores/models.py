from pydantic import BaseModel
from datetime import date

class TrabajadorBase(BaseModel):
    Nombre: str
    FechaContrato: date
    AnosRestantes: int
    Cargo: str
    DiasProgresivosBase: int
    Estado: bool

class TrabajadorCrear(TrabajadorBase):
    RutTrabajador: str

class TrabajadorActualizar(TrabajadorBase):
    pass

class Trabajador(TrabajadorCrear):
    Estado: bool