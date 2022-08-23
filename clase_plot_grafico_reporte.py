
#import matplotlib
from matplotlib import use
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as Navi
#import numpy as np
from re import findall

use('Qt5Agg')
from matplotlib.ticker import FormatStrFormatter

class GraficoReport(Canvas):
    def __init__(self,
                 parent=None,
                 matriz=None,
                 tabla=None,
                 eje_x_graf=None,
                 eje_y_graf=None,
                 titulo=None,
                 eje_x_legend=None,
                 eje_y_legend=None,
                 figsize=None,
                 dpi=70,
                 current_text_combobox=None,
                 actualizar=None,
                 decimales_y=None,
                 checkboxes=None,
                 ):

        self.fig, self.ax = plt.subplots(dpi=dpi, figsize=figsize)
        super(GraficoReport, self).__init__(self.fig)

        self.setParent(parent)
        self.current_text_combobox = current_text_combobox # Texto actual de la combobox que muestra si se grafica SG o palpador
        self.tabla = tabla              # Recibe la tabla pandas de la cual se sacara la informacion
        self.matriz = matriz            # Recibe una tupla con los elementos posibles a graficar
        self.eje_x_graf = eje_x_graf    # Recibe una lista donde cada index corresponde a los valores de un eje X
        self.eje_y_graf = eje_y_graf    # Recibe una lista donde cada index corresponde a los valores de un eje Y, podria estar mejor optimizado pero es como lo mismo
        self.titulo = titulo            # Titulo del gráfico
        self.eje_x_legend = eje_x_legend
        self.eje_y_legend = eje_y_legend
        self.actualizar = actualizar
        self.decimales_y = decimales_y
        self.checkboxes = checkboxes


        #     MATRIZ ES LA SIGUIENTE
        #     self.deformaciones_agregadas = (
        #     (self.def_SG_1_creada, 'Def Axial SG 1', 'Def Diametral SG 1', 'Strain Gauges 1', ' Corregida','Def Volumetrica SG 1'),
        #     (self.def_SG_2_creada, 'Def Axial SG 2', 'Def Diametral SG 2', 'Strain Gauges 2', ' Corregida', 'Def Volumetrica SG 2'),
        #     (self.def_PP_creada, 'Def Axial PP', 'Def Diametral PP', 'Palpadores', 'Corregida', 'Def Volumetrica PP')

        self.paleta = ['blue', 'orange', 'green', 'red']



    def graficar(self):

        try:
            plt.close(self.fig)
        except:
            pass

        try:
            for i in range(0, len(self.ax.lines)):
                del self.ax.lines[-1]
        except IndexError:
            pass

        contador = 0
        for x, y in zip(self.eje_x_graf, self.eje_y_graf):

            if self.checkboxes[contador].isChecked():
                self.ax.plot(x*4 if contador < 3 else x,
                             y,
                             #label='SG' if contador == 0 else ("SG Corregido" if contador == 3 else ("PP" if contador == 6 else ("PP Corregido" if contador == 9 else ""))),
                             label='SG' if findall("SG 1$",self.checkboxes[contador].text()) and contador % 3 == 0 else\
                                 ('SG Corregido' if findall("SG 1 Corregida", self.checkboxes[contador].text()) and contador % 3 == 0 else \
                                 ('PP' if findall("PP$", self.checkboxes[contador].text()) and contador % 3 == 0 else (
                                 ('PP Corregido' if findall("PP Corregida", self.checkboxes[contador].text()) and contador % 3 == 0 else ''
                                 )))),
                             color='orange' if contador < 3 else ('blue' if contador < 6 else ('brown' if contador <9 else ('green' if contador <12 else 'black'))))
            contador+=1
        self.ax.set(xlabel = self.eje_x_legend, ylabel = self.eje_y_legend,
                    title = f'Curva Esfuerzo Deformacion' if self.titulo is None else self.titulo)

        self.ax.grid(linewidth=1)
        self.fig.tight_layout()
        self.ax.relim()
        self.ax.autoscale()
        self.ax.legend()
        self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        self.fig.savefig('recursos/images.temp/figura_reporte_plt.png')




