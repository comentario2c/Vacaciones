from pydantic import BaseModel
from datetime import date

class FeriadoCreate(BaseModel):
    fecha: date
    nombre: str

class FeriadoUpdate(BaseModel):
    fecha: date
    nombre: str

class FeriadoOut(BaseModel):
    ID_FeriadosNacionales: int
    Fecha: date
    Nombre: str