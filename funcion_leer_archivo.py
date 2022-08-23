import sys
import os


def func_leer_archivo(ruta_archivo):

    if ruta_archivo is not None:

        try:
            os.remove("recursos/txt.txt")
        except FileNotFoundError:
            pass

        try:
            os.remove("recursos/headers.txt")
        except FileNotFoundError:
            pass

        archivo = open(ruta_archivo,
                            "r")
        file = open("recursos/txt.txt", "w")

        for x in archivo:
            xf = x.replace(",", "")
            file.write(xf)
        archivo.close()
        file.close()

        archivo = open("recursos/txt.txt", "r")
        lineas = archivo.readlines()

        archivo.close()

        header = lineas[2].split(";")

        del lineas
        for i in header:
            if i == "\n":
                header.remove(i)
        for i in header:
            if i == "Hora":
                header.remove(i)

        rows_encabezados = len(header)

        # CREAR ARCHIVO DE TEXTO PARA ALMACENAR LAS COLUMNAS
        with open(
                "recursos/headers.txt",
                "w",
                encoding="utf-8"
        ) as f:
            for linea in header:
                f.write(linea)
                if linea != rows_encabezados - 1:
                    f.write('\n')


        return header, rows_encabezados