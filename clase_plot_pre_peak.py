
#import matplotlib
from matplotlib import use
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as Navi
#import numpy as np

use('Qt5Agg')
from matplotlib.ticker import FormatStrFormatter

class Grafico(Canvas):
    def __init__(self,
                 parent=None,
                 matriz=None,
                 tabla=None,
                 eje_x_graf=None,
                 eje_y_graf=None,
                 # eje_x_graf_2 = None,
                 # eje_y_graf_2 = None,
                 titulo=None,
                 eje_x_legend=None,
                 eje_y_legend=None,
                 figsize=None,
                 dpi=100,
                 current_text_combobox=None,
                 actualizar=None,
                 decimales_y=None
                 ):

        self.fig, self.ax = plt.subplots(dpi=dpi, figsize=figsize)
        super(Grafico, self).__init__(self.fig)

        self.setParent(parent)
        self.current_text_combobox = current_text_combobox # Texto actual de la combobox que muestra si se grafica SG o palpador
        self.tabla = tabla              # Recibe la tabla pandas de la cual se sacara la informacion
        self.matriz = matriz            # Recibe una tupla con los elementos posibles a graficar
        self.eje_x_graf = eje_x_graf    # Recibe una lista con los combobox que contienen el texto de los ejes
        self.eje_y_graf = eje_y_graf    # Recibe una lista de 1 valor con los combobox que contienen el texto de los ejes
        self.titulo = titulo            # Titulo del gráfico
        self.eje_x_legend = eje_x_legend
        self.eje_y_legend = eje_y_legend
        self.actualizar = actualizar
        self.decimales_y = decimales_y


        #     MATRIZ ES LA SIGUIENTE
        #     self.deformaciones_agregadas = (
        #     (self.def_SG_1_creada, 'Def Axial SG 1', 'Def Diametral SG 1', 'Strain Gauges 1', ' Corregida','Def Volumetrica SG 1'),
        #     (self.def_SG_2_creada, 'Def Axial SG 2', 'Def Diametral SG 2', 'Strain Gauges 2', ' Corregida', 'Def Volumetrica SG 2'),
        #     (self.def_PP_creada, 'Def Axial PP', 'Def Diametral PP', 'Palpadores', 'Corregida', 'Def Volumetrica PP')

        self.paleta = ['blue', 'orange', 'green', 'red']

        try:
            plt.close(self.fig)
        except:
            pass

        try:
            for i in range(0, len(self.ax.lines)):
                del self.ax.lines[-1]
        except IndexError:
            pass

    def graficar(self):
        label = [1, 2, 5]
        for i in range(0, 3):
            if self.matriz[i][0]:
                if self.current_text_combobox == self.matriz[i][3] or self.current_text_combobox == self.matriz[i][3] + self.matriz[i][4] :
                    for column in self.eje_x_graf:
                        self.ax.plot(self.tabla[column.currentText()],
                                     self.tabla[self.eje_y_graf[0].currentText()],
                                     color = self.paleta[self.eje_x_graf.index(column)],
                                     label= column.currentText(),
                                     #label = self.matriz[i][label[self.eje_x_graf.index(column)]]
                                     )
                    self.ax.set(xlabel=self.eje_x_legend, ylabel=self.eje_y_legend,
                                title=f"Curva Esf-Def - {self.matriz[i][3]}" if self.titulo is None else self.titulo)

        if self.actualizar != 'si':
            self.fig.tight_layout()
            self.ax.grid()

        self.fig.tight_layout()
        self.ax.relim()
        self.ax.autoscale()
        self.ax.legend()
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(self.decimales_y))
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))




