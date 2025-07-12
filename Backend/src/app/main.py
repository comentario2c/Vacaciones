from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importar dependencias de auth
from app.auth.dependiences import requiere_rol

# Conexion a la base de datos
from app.db.db import get_connection

# Routers
from app.auth.routes import router as auth_router
from app.crud.permisos.routes import router as permisos_router
from app.crud.trabajadores.routes import router as trabajadores_router
from app.crud.movimientoVacaciones.routes import router as movimiento_vacaciones_router

app = FastAPI()

def db_dependency():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

@app.get("/api/test-db")
def test_db(conn=Depends(db_dependency)):
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    if result and result[0] == 1:
        return {"status": "OK"}
    raise HTTPException(500, "Error en consulta de prueba")

@auth_router.get("/solo-admin")
def ruta_admin(usuario=Depends(requiere_rol(["admin"]))):
    return {"msg": f"Acceso otorgado a {usuario['rol']}"}

@auth_router.get("/ver-informacion")
def ruta_general(usuario=Depends(requiere_rol(["admin", "secretaria", "gestor"]))):
    return {"msg": f"Información visible para {usuario['rol']}"}


# CORS middleware para permitir solicitudes desde el frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(trabajadores_router, prefix="/api/trabajadores", tags=["trabajadores"])
app.include_router(movimiento_vacaciones_router, prefix="/api/vacaciones", tags=["vacaciones"])
app.include_router(permisos_router, prefix="/api/permisos", tags=["permisos"])