from fastapi import FastAPI, Depends, HTTPException
from app.db.db import get_connection

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