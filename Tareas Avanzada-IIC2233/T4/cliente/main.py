import sys, json, os
from PyQt5.QtWidgets import QApplication
from backend.cliente import Client
from frontend.login_window import Ventana_login
from frontend.main_window import Ventana_Archivos, Ventana_Descargas
from parametros import JSON_FILE

class DCComparte_Archivos:

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.port = port
        self.ventana_login = Ventana_login()
        self.ventana_main_d = Ventana_Descargas()
        self.ventana_main_a = Ventana_Archivos()
        self.client = Client(**data)

    # Señales
        # Señales login
        self.ventana_login.senal_crear_cliente.connect(self.client.conectar_al_servidor)
        self.client.senal_success.connect(self.ventana_login.entrar_sitio)
        self.ventana_login.senal_entrar_sitio.connect(self.ventana_main_d.login_success)
        self.client.senal_fail.connect(self.ventana_login.login_fallido)
        # Señales menús
        self.ventana_main_d.senal_cambiar_ventana.connect(self.ventana_main_a.mostrar_archivos)
        self.ventana_main_a.senal_cambiar_ventana.connect(self.ventana_main_d.mostrar_descargas)
        self.client.senal_actualizar.connect(self.ventana_main_d.actualizar_lista)
        self.client.senal_actualizar_archivos.connect(self.ventana_main_d.actualizar_lista_archivos)
        self.ventana_main_d.senal_descargar_archivo.connect(self.client.solicitar_descarga)

        # Señales de desconexión de cliente
        self.ventana_main_d.senal_desconexion.connect(self.client.desconectar)
        self.ventana_main_d.senal_desconexion.connect(self.client.desconectar)

if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    try:
        port = int(sys.argv[1])
    except:
        print("Escribe un port válido\n0-65535")

    path = os.path.join(JSON_FILE)
    with open(path) as f:
        data = json.load(f)
    data["port"] = port

    app = QApplication(sys.argv)
    dccomparte_archivos = DCComparte_Archivos(data)

    sys.exit(app.exec())