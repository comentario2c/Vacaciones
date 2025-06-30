from mysql.connector import pooling, Error
from app.core.config import settings

pool = pooling.MySQLConnectionPool(
    pool_name = "vac_pool",
    pool_size = 5,
    host      = settings.DB_HOST,
    port      = settings.DB_PORT,
    user      = settings.DB_USER,
    password  = settings.DB_PASSWORD,
    database  = settings.DB_NAME
)

def get_connection():
    try:
        return pool.get_connection()
    except Error as e:
        print("Error al obtener conexión:", e)
        raise