from fastapi import FastAPI, Depends, HTTPException
from app.db.db import get_connection
from app.auth.routes import router as auth_router
from app.auth.dependiences import requiere_rol
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

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