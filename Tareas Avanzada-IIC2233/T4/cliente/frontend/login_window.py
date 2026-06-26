import sys, os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton,
                             QLineEdit, QVBoxLayout)
import time

class Ventana_login(QWidget):
    senal_login = pyqtSignal()
    senal_crear_cliente = pyqtSignal(str)
    senal_entrar_sitio = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.init_gui()

    def init_gui(self) -> None:
        self.setWindowTitle('DCComparte Archivos')

        layout = QVBoxLayout()
        layout.addStretch()

        self.texto1 = QLabel('Ingrese su nombre de usuario con:\n'
                               'Al menos 1 mayúscula\n' 
                               'Al menos 1 numero \ny entre 3 y 16'
                               ' caracteres de largo', self)
        layout.addWidget(self.texto1)
        self.texto1.resize(self.texto1.sizeHint())

        self.input = QLineEdit('Nombre de usuario', self)
        layout.addWidget(self.input)
        self.input.resize(self.input.sizeHint())

        self.conectar = QPushButton('Conectar', self)
        self.conectar.clicked.connect(self.boton_clickeado)
        layout.addWidget(self.conectar)

        self.resultado = QLabel('', self)
        layout.addWidget(self.resultado)
        self.resultado.resize(self.resultado.sizeHint())

        self.setGeometry(800, 450, 400, 250)
        layout.addStretch()
        self.setLayout(layout)
        self.show()

    def boton_clickeado(self) -> None:
        """Envía señal para empezar la conexión"""
        texto_input = self.input.text()
        self.senal_crear_cliente.emit(texto_input)
        self.senal_login.emit()

    def entrar_sitio(self, texto: str) -> None:
        for i in range(4):
            self.resultado.setText(texto + ".." * i)
            self.resultado.resize(self.resultado.sizeHint())
            self.resultado.repaint()
            time.sleep(1)
        self.hide()
        self.senal_entrar_sitio.emit()

    def login_fallido(self, texto: str) -> None:
        self.resultado.setText(texto)
        self.resultado.resize(self.resultado.sizeHint())
        self.resultado.repaint()
