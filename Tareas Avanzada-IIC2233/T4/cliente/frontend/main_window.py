import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QAction, QTableWidget,
                             QProgressBar, QVBoxLayout, QMainWindow, QGridLayout, QListWidget,
                             QLineEdit, QTableWidgetItem, QScrollArea, QHeaderView)
from PyQt5.QtGui import QIcon

class Ventana_Descargas(QMainWindow):
    onchange_status_bar = pyqtSignal(str)
    senal_cambiar_ventana = pyqtSignal()
    senal_desconexion = pyqtSignal()
    senal_descargar_archivo = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.lista_usuarios_conectados = []

        self.setWindowTitle("DCComparte Archivos")
        self.setGeometry(600, 200, 1000, 800)
        
        path = os.path.join('images', 'logo_DCComparte.jpg')
        self.setWindowIcon(QIcon(path))

        """Barra de menú."""
        menubar = self.menuBar()
        menu_descargas = menubar.addMenu("Mis Descargas")

        menu_archivos = menubar.addMenu("Mis Archivos")
        accion_admin_descargas = QAction("Cambiar a este menu", self)
        menu_archivos.addAction(accion_admin_descargas)
        accion_admin_descargas.triggered.connect(self.cambiar_ventana)

        """Barra de herramientas."""
        search_bar = self.addToolBar("Buscar Archivos")
        self.addToolBar(search_bar)

        self.search_solicitud = QLineEdit('Nombre del archivo', self)
        search_bar.addWidget(self.search_solicitud)
        boton_buscar = QAction("Buscar", self)
        search_bar.addAction(boton_buscar)

        """Main Widget."""
        self.main_widget = QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        main_layout = QGridLayout(self.main_widget)
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(3)
        self.download_table.setHorizontalHeaderLabels(['Nombre', 'Tamaño', 'Estado'])
        self.download_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.download_table.verticalHeader().setVisible(False)
        self.download_table.setRowCount(8) 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.download_table)

        self.progreso = QVBoxLayout()
        self.barras = []
        for i in range(5):
            barra = QProgressBar()
            barra.setValue((i+1)*20)  # Valores de ejemplo
            self.barras.append(barra)
            self.progreso.addWidget(QLabel(f"Descarga {i+1}:"))
            self.progreso.addWidget(barra)

        estado = QWidget()
        estado.setLayout(self.progreso)

        self.lista_usuarios = QListWidget()

        botones_layout = QVBoxLayout()
        self.boton_descargar = QPushButton("Descargar")
        self.boton_descargar.setEnabled(False)
        self.boton_descargar.clicked.connect(self.solicitar_descarga_archivo)
        self.boton_pausar = QPushButton("Pausar")
        self.boton_cancelar = QPushButton("Cancelar")
        botones_layout.addWidget(self.boton_descargar)
        botones_layout.addWidget(self.boton_pausar)
        botones_layout.addWidget(self.boton_cancelar)
        botones = QWidget()
        botones.setLayout(botones_layout)

        self.download_table.itemSelectionChanged.connect(self.habilitar_boton_descarga)

        main_layout.addWidget(self.download_table, 0, 0, 1, 2)
        main_layout.addWidget(estado, 0, 2)
        main_layout.addWidget(self.lista_usuarios, 1, 0, 1, 2)
        main_layout.addWidget(botones, 1, 2)

        main_layout.setColumnStretch(0, 2)#Asi el widget de descargas
        main_layout.setColumnStretch(1, 2)#usa el doble de espacio
        main_layout.setColumnStretch(2, 1)
        main_layout.setRowStretch(0, 2)
        main_layout.setRowStretch(1, 1)

    def login_success(self) -> None:
        self.show()

    def mostrar_descargas(self) -> None:
        self.show()

    def cambiar_ventana(self) -> None:
        self.hide()
        self.senal_cambiar_ventana.emit()

    def closeEvent(self, event):
        self.senal_desconexion.emit()
        event.accept()

    def actualizar_lista(self, users, command) -> None: 
        """
        Actualiza la lista de usuarios conectados.
        """
        if command == 'add':
            for user in users:
                if user not in self.lista_usuarios_conectados:
                    self.lista_usuarios.addItem(user)
                    self.lista_usuarios_conectados.append(user)
    
    def actualizar_lista_archivos(self, archivos: list):
        """
        Actualiza la lista de archivos mostrados en la ventana.
        """
        self.download_table.setRowCount(len(archivos))
        for i, (archivo, tamaño) in enumerate(archivos):
            item_nombre = QTableWidgetItem(archivo)
            item_tamaño = QTableWidgetItem(f"{tamaño} bytes")
            item_estado = QTableWidgetItem("Disponible")
            
            self.download_table.setItem(i, 0, item_nombre)
            self.download_table.setItem(i, 1, item_tamaño)
            self.download_table.setItem(i, 2, item_estado)

    def habilitar_boton_descarga(self):
        """
        Activa el boton de descarga si se elige un archivo.
        """
        seleccion = self.download_table.selectedItems()
        self.boton_descargar.setEnabled(bool(seleccion))
    
    def solicitar_descarga_archivo(self):
        seleccion = self.download_table.selectedItems()
        if seleccion:
            archivo = seleccion[0].text()  # columna 0 = nombre
            self.senal_descargar_archivo.emit(archivo)

class Ventana_Archivos(QMainWindow):
    onchange_status_bar = pyqtSignal(str)
    senal_cambiar_ventana = pyqtSignal()
    senal_desconexion = pyqtSignal()
    senal_abrir_archivo = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("DCComparte Archivos")
        self.setGeometry(600, 200, 1000, 800)
        
        path = os.path.join('images', 'logo_DCComparte.jpg')
        self.setWindowIcon(QIcon(path))

        # Lista de archivos
        self.lista_archivos = QListWidget(self)
        self.setCentralWidget(self.lista_archivos)

        # Botón para abrir archivo
        self.boton_abrir = QPushButton("Abrir")
        self.boton_abrir.setEnabled(False)
        self.boton_abrir.clicked.connect(self.abrir_archivo)

        layout = QVBoxLayout()
        layout.addWidget(self.lista_archivos)
        layout.addWidget(self.boton_abrir)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.lista_archivos.itemSelectionChanged.connect(self.habilitar_boton_abrir)

        """Barra de menú."""
        menubar = self.menuBar()
        menu_descargas = menubar.addMenu("Mis Descargas")
        accion_admin_descargas = QAction("Cambiar a este menu", self)
        menu_descargas.addAction(accion_admin_descargas)
        accion_admin_descargas.triggered.connect(self.cambiar_ventana)

        menu_archivos = menubar.addMenu("Mis Archivos")

        """Barra de herramientas."""
        search_bar = self.addToolBar("Buscar Archivos")
        self.addToolBar(search_bar)

        self.search_solicitud = QLineEdit('Nombre del archivo', self)
        search_bar.addWidget(self.search_solicitud)
        boton_buscar = QAction("Buscar", self)
        search_bar.addAction(boton_buscar)
        
    def cambiar_ventana(self) -> None:
        self.hide()
        self.senal_cambiar_ventana.emit()

    def mostrar_archivos(self) -> None:
        self.show()
    
    def actualizar_lista_archivos(self, archivos: list):
        self.lista_archivos.clear()
        self.lista_archivos.addItems(archivos)

    def habilitar_boton_abrir(self):
        seleccion = self.lista_archivos.selectedItems()
        self.boton_abrir.setEnabled(bool(seleccion))

    def abrir_archivo(self):
        seleccion = self.lista_archivos.selectedItems()
        if seleccion:
            nombre_archivo = seleccion[0].text()
            ruta_archivo = os.path.join("mis_archivos", nombre_archivo)
            if os.path.exists(ruta_archivo):
                os.startfile(ruta_archivo)
            else:
                pass
    
    def closeEvent(self, event):
        self.senal_desconexion.emit()
        event.accept()

