from app.db.db import get_connection
from mysql.connector import Error

def obtener_configuracion_vacaciones() -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Clave, Valor FROM ConfiguracionVacaciones;")
        filas = cursor.fetchall()
        config_raw = {clave: valor for clave, valor in filas}

        claves_requeridas = {
            "DíasBaseAnuales": "dias_base_anuales",
            "AñosParaPrimerProgresivo": "anios_para_primer_progresivo",
            "AñosParaProgresivoEmpresa": "anios_para_progresivo_empresa",
            "PeriodoEntreProgresivos": "periodo_entre_progresivos"
        }

        for clave in claves_requeridas:
            if clave not in config_raw:
                raise ValueError(f"[Configuración Vacaciones] Falta la clave obligatoria en BD: '{clave}'")

        return {
            alias: int(config_raw[clave])
            for clave, alias in claves_requeridas.items()
        }

    except Error as e:
        print("Error al consultar ConfiguracionVacaciones:", e)
        raise

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()