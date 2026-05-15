import time

def esBisiesto(anno):
    """
    Funcionamiento:
    Determina si un año es bisiesto intentando crear la fecha 29 de febrero.
    Entradas:
    Un número entero (el año).
    Salidas:
    True si es bisiesto, False si no lo es.
    """
    try:
        # Intentamos crear una estructura de tiempo para el 29 de febrero de ese año
        # Formato: (Año, Mes, Día, Hora, Min, Seg, Día_semana, Día_año, Horario_verano)
        time.struct_time((anno, 2, 29, 0, 0, 0, 0, 0, -1))
        return True
    except ValueError:
        # Si el sistema dice que el valor es inválido, es porque el año NO es bisiesto
        return False