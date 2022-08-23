import pandas as pd
from time import time
from pandas import read_csv

from pandas import options
options.mode.chained_assignment = None


def crear_tabla_inicial(checkbuttons=None,
                        headers=None):

    tabla = read_csv(
        filepath_or_buffer="Recursos/txt.txt",
        delimiter=';',
        skiprows=3,
        skipfooter=7,
        index_col=False,
        engine='python'
    )
    tabla.columns = headers

    for i in range(0, len(headers)):
        if 0 >= i > len(headers)-1:
            tabla = tabla.astype({
                headers[i]: float,
            })

    try:
        tabla.to_csv("recursos/tabla_original.csv", index=False)
    except PermissionError:
        pass

    return tabla

