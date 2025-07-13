from datetime import date

def calcular_dias_progresivos(fecha_contrato: date, anos_restantes: int, anio_consulta: int) -> int:
    año_ingreso = fecha_contrato.year
    año_progresivo = año_ingreso + anos_restantes

    if anio_consulta >= año_progresivo:
        return 1 + ((anio_consulta - año_progresivo) // 3)
    return 0
