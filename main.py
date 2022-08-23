# import numpy as np
from PyQt5 import QtWidgets

from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal, QRect
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap

import sys
import os

import time
#import pandas as pd

#from math import pi
#from matplotlib.widgets import SpanSelector
#from scipy import stats
#from re import findall

#from openpyxl import load_workbook
#from openpyxl.utils import get_column_letter
#from openpyxl.chart import Reference, ScatterChart

from pandas import options
import ctypes

from splash_window import Ui_splash_window
from interfaz_main_window import Ui_MainWindow

from funcion_leer_archivo import func_leer_archivo
from funcion_crear_tabla_inicial import crear_tabla_inicial
from funcion_cargar_tabla_en_visualizador import pandasModel

options.mode.chained_assignment = None
id_app = 'SFlores.Geomechanics.EnsayosUCS.V1.05'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(id_app)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()

        # self.splash = QtWidgets.QSplashScreen()
        self.screen = Ui_splash_window()
        self.screen.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        pixmap = QPixmap("recursos/Images/icon_resized.png")
        self.setPixmap(pixmap)
        self.show()
        self.progress()

    def progress(self):
        for i in range(100):
            time.sleep(0.1)
            self.screen.progressBar.setValue(i)


class VentanaPrincipal:

    #resized = pyqtSignal()

    def __init__(self):

        self.ventana_principal = QtWidgets.QMainWindow()
        self.ventana_principal.setWindowIcon(QIcon("recursos/Images/icon.png"))

        self.vp = Ui_MainWindow()
        self.vp.setupUi(self.ventana_principal)
        self.ventana_principal.show()

        # Variables a crear para la funcion obtener_ruta_archivo
        self.ruta_archivo_txt = None
        self.nombre_archivo_txt = None
        self.header = None
        self.rows_encabezados = None
        self.tabla_con_deformaciones = []  # quizá la deberia borrar (?)
        self.tabla_mod_elasticos = []  # quiza la deberia borrar (?)
        self.tabla_completa = None
        self.vp.tabla_completa = None

        # CONTADORES Y VALIDADORES FUNCION IMPORTAR ARCHIVO
        self.adv_header_y_defs = True

        # Variables para la funcion de reportar imagenes:
        self.ruta_archivo_imagen = None
        self.nombre_archivo_imagen = None

        # BOTONES DE IMPORTACION A TABLA
        self.vp.button_importarArchivo.clicked.connect(lambda: self.obtener_ruta_archivo(self.ruta_archivo_txt))
        self.vp.button_agregar_a_tabla.clicked.connect(lambda: self.asignar_header_y_deformaciones())

        # BOTONES DE OPERACIONES EN LA TABLA
        self.vp.pushButton.clicked.connect(lambda: self.cambiar_signo_deformacion())
        self.vp.pushButton_3.clicked.connect(lambda: self.corregir_deformacion())
        self.vp.pushButton_7.clicked.connect(lambda: self.filtrar_tabla_completa())
        self.vp.pushButton_8.clicked.connect(lambda: self.restablecer_tabla_completa())

        # Manejo de Eventos - Falta agregar varias funciones aca
        self.vp.tabWidget.currentChanged.connect(lambda: self.hola())

        # BOTONES DE OPERACIONES EN GRAFICO

        self.vp.pushButton_6.clicked.connect(lambda: self.seleccion_manual())
        self.vp.pushButton_2.clicked.connect(lambda: self.vp.graficos())

        # BOTONES DE REPORTE

        self.vp.pushButton_imagen_previa.clicked.connect(lambda: self.cargar_imagenes(ruta=self.ruta_archivo_imagen,
                                                                                      label_destino=self.vp.label_imagen_previa,
                                                                                      estado='pre'))
        self.vp.pushButton_imagen_posterior.clicked.connect(lambda: self.cargar_imagenes(ruta=self.ruta_archivo_imagen,
                                                                                         label_destino=self.vp.label_imagen_posterior,
                                                                                         estado='post'))


    # def resizeEvent(self, event):
    #     self.resized.emit()
    #     return super(VentanaPrincipal, self).resizeEvent(event)

    # def resizeFunction(self):
    #     self.vp.widget_2.setGeometry(QRect(0, 0, self.width(), self.height() - 20))
    #     self.vp.chart.setGeometry(QRect(0, 0, self.width(), self.height() - 30))

    def hola(self):
        if self.vp.tabWidget.currentIndex() == 3:
            self.adv_header_y_defs = False

    # Funciones para importar y visualizar tabla

    def obtener_ruta_archivo(self, ruta=None):

        self.ruta_archivo_txt = None
        file_filter = "Archivo de Texto (*.txt)"
        self.ruta_archivo_txt, _ = QtWidgets.QFileDialog.getOpenFileName(
            caption="Elige un Archivo",
            directory=ruta if ruta is not None else os.getcwd(),
            filter=file_filter,
            initialFilter='Archivo de Texto (*.txt)'
        )

        if self.ruta_archivo_txt:
            self.nombre_archivo_txt = os.path.splitext(os.path.basename(self.ruta_archivo_txt))[0]
            self.vp.label_nombre_archivo.setText(str(self.nombre_archivo_txt))
            self.vp.lineEdit_codigo_muestra.setText(str(self.nombre_archivo_txt))

            self.header, self.rows_encabezados = func_leer_archivo(self.ruta_archivo_txt)

            self.tabla_con_deformaciones = []
            self.tabla_mod_elasticos = []

            self.tabla_completa = crear_tabla_inicial(headers=self.header)
            self.vp.crear_checkbuttons(self.header)

            self.vp.agregar_esfuerzo_a_tabla_completa(header=self.header)
            self.vp.obtener_esf_peak()
            self.vp.obtener_tabla_pre_peak()
            self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)
            self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
            # self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)

            self.contador_advertencia_dimensiones = 0
            self.adv_header_y_defs = True

            # BORRAR ARCHIVOS TEMPORALES DE IMAGENES

            if len(os.listdir('recursos/images.temp')) > 0:
                warning = self.warning(f"¿Deseas eliminar las imagenes temporales almacenadas de ensayos anteriores?\n"
                                       f"Hay {len(os.listdir('recursos/images.temp'))} imagenes que puedes revisar en la carpeta 'recursos/images.temp'")
                if warning:
                    filelist = [f for f in os.listdir('recursos/images.temp') if f.endswith(".png")]
                    for f in filelist:
                        os.remove(os.path.join('recursos/images.temp', f))


        return

    def visualizar_tabla(self, tabla_a_mostrar, widget):
        self.model = pandasModel(tabla_a_mostrar)
        self.view = widget
        self.view.setModel(self.model)
        self.view.show()
        return

    def asignar_header_y_deformaciones(self):
        if self.ruta_archivo_txt is not None:
            if self.adv_header_y_defs:
                self.adv_header_y_defs = self.warning("No has cambiado las dimensiones de la probeta\n¿Deseas Hacerlo?")
                if self.adv_header_y_defs:
                    self.vp.tabWidget.setCurrentIndex(3)
                elif not self.adv_header_y_defs:
                    self.asignar_header_y_deformacioness()
                self.adv_header_y_defs = False
            else:
                self.asignar_header_y_deformacioness()

    def asignar_header_y_deformacioness(self):

        self.correccion_deformaciones = 'no'
        self.vp.asignar_headers()
        self.vp.agregar_esfuerzo_a_tabla_completa(header=self.header)
        self.vp.agregar_def_porcentuales_a_tabla()
        self.vp.agregar_def_finales_a_tabla()
        self.vp.obtener_esf_peak()
        self.vp.asinar_opciones_combobox_signo_deformacion()
        self.vp.agregar_def_volumetricas()
        self.vp.asinar_opciones_combobox_filtrar_tabla_completa()
        self.vp.obtener_tabla_pre_peak()
        self.vp.respaldo_tabla_completa()

        self.vp.graficar_reporte(matriz=None)

        #self.vp.graficos()
        self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
        self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)

        self.vp.widget_2.setUpdatesEnabled(True)
        self.vp.graficos()

        self.vp.agrupar_elementos_reporte()
        self.vp.signal_reporte_combobox_opciones()
        self.vp.comboBox_tipo_ensayo.setCurrentIndex(1)

        QCoreApplication.processEvents()

    #Funciones para operaciones con tablas

    def cambiar_signo_deformacion(self):
        if self.vp.tabla_completa is not None:
            if len(self.vp.tabla_completa) > 0:
                if self.vp.comboBox.count() > 0:
                    self.vp.tabla_completa[self.vp.comboBox.currentText()] = -self.vp.tabla_completa[
                        self.vp.comboBox.currentText()]

                    self.vp.tabla_pre_peak[self.vp.comboBox.currentText()] = -self.vp.tabla_pre_peak[
                        self.vp.comboBox.currentText()]

                    self.vp.agregar_def_volumetricas()
                    self.vp.obtener_tabla_pre_peak()
                    self.vp.graficar_reporte(matriz=None)

                    self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
                    self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)

                    self.vp.graficos()

    def corregir_deformacion(self):
        if self.vp.tabla_completa is not None:
            if len(self.vp.tabla_completa) > 50000:
                advertencia = self.warning(
                    f"El archivo de texto tiene {len(self.vp.tabla_completa)} columnas, esta operación\npodría tomar varios minutos\n"
                    f"¿Deseas continuar?")
                if not advertencia:
                    return

            self.correccion_deformaciones = 'si'
            self.vp.funcion_corregir_deformacion()

            self.vp.agregar_def_volumetricas()
            self.vp.obtener_tabla_pre_peak()
            self.vp.asinar_opciones_combobox_filtrar_tabla_completa()

            self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
            self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)
            self.vp.asignar_opciones_combobox_graficos(matriz=self.vp.deformaciones_agregadas,
                                                       correccion_defs='si')
            self.vp.graficar_reporte(matriz=None)

    def filtrar_tabla_completa(self):
        if self.ruta_archivo_txt is not None:

            if self.vp.lineEdit_filtro_min.text() == '':
                self.vp.lineEdit_filtro_min.setText(str(self.vp.tabla_completa[self.vp.comboBox_9.currentText()].min()))
            if self.vp.lineEdit_filtro_max.text() == '':
                self.vp.lineEdit_filtro_max.setText(str(self.vp.tabla_completa[self.vp.comboBox_9.currentText()].max()))


            self.vp.filtrar_tabla_completa()
            self.vp.obtener_tabla_pre_peak()

            self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
            self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)

            self.vp.graficos()
            self.vp.graficar_reporte(matriz=None)

    def restablecer_tabla_completa(self):
        if self.ruta_archivo_txt is not None:

            self.vp.restablecer_tabla_completa()
            self.vp.obtener_tabla_pre_peak()

            self.visualizar_tabla(self.vp.tabla_completa, self.vp.tableView_Datos_completos)
            self.visualizar_tabla(self.vp.tabla_pre_peak, self.vp.tableView_Datos)

            self.vp.graficos()
            self.vp.graficar_reporte(matriz=None)

    # Funciones para apartado grafico

    def seleccion_manual(self):

        self.vp.widget_2.hide()
        self.vp.widget_3.hide()

        self.vp.seleccionar_area_manual()

        self.vp.widget_2.show()
        self.vp.widget_3.show()

    # Funciones para apartado reportes

    def cargar_imagenes(self, ruta=None, label_destino=None, estado=None):
        self.ruta_archivo_imagen = None
        file_filter = "Imagen (*.png *.jpg *.jpeg)"
        self.ruta_archivo_imagen, _ = QtWidgets.QFileDialog.getOpenFileName(
            caption="Elige un Archivo",
            directory=ruta if ruta is not None else os.getcwd(),
            filter=file_filter,
            initialFilter='Imagen (*.png *.jpg *.jpeg)'
        )
        if self.ruta_archivo_imagen:

            self.vp.rotar_imagen(ruta=self.ruta_archivo_imagen)
            self.nombre_archivo_imagen = os.path.splitext(os.path.basename(self.ruta_archivo_imagen))[0]

            self.ruta_imagen_dimensionada = self.vp.redimensionar_imagen(ruta=self.ruta_archivo_imagen,
                                         dimensiones=(280, 280),
                                         nombre=self.nombre_archivo_imagen,
                                         estado=estado)


            pixmap = QPixmap(self.ruta_imagen_dimensionada)

            label_destino.setPixmap(pixmap)

        return

    def reporte(self):


        pass


    def warning(self, texto):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Advertencia")
        dlg.setText(texto)
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # ICONO EN PANEL INFERIOR DERECHO
    trayIcon = QSystemTrayIcon(QIcon("recursos/Images/icon.png"), parent=app)
    trayIcon.setToolTip("Ensayos UCS y Post Peak")
    trayIcon.show()
    menu_taskbar = QMenu()
    exitAction = menu_taskbar.addAction("Cerrar")
    exitAction.triggered.connect(app.quit)
    trayIcon.setContextMenu(menu_taskbar)
    # ICONO EN PANEL INFERIOR DERECHO

    # ACTIVAR splash CUANDO VAYA A GENERAR EJECUTABLES
    #splash = SplashScreen()

    window = VentanaPrincipal()
    #splash.finish(splash)
    sys.exit(app.exec_())
