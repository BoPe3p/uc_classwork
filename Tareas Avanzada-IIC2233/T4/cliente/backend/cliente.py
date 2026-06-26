import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import json, sys, os, threading
from parametros import SIZE_BUFFER

class Client(QObject):
    senal_success = pyqtSignal(str)
    senal_fail = pyqtSignal(str)
    senal_actualizar = pyqtSignal(list, str)
    senal_actualizar_archivos = pyqtSignal(list)

    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.thread_descarga = None
        self.thread_escucha = None
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
        #Lo anterior es para ver los prints en tiempo real!!

    def conectar_al_servidor(self, nombre_usuario) -> None:
        valid = validar_usuario(nombre_usuario)
        if valid:
            try:
                # Creamos un socket nuevo para cada cliente
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.socket.connect((self.host, self.port))
                self.socket.sendall(nombre_usuario.encode('utf-8'))
                respuesta = self.socket.recv(1024).decode('utf-8')

                if respuesta == "Usuario existente":
                    self.senal_fail.emit('Error al ingresar,\nUsuario existente...')
                    self.desconectar()
                    return

                print("Cliente conectado exitosamente al servidor.")
                self.senal_success.emit(f"Bienvenido {nombre_usuario}\nConectando")
                self.senal_actualizar.emit([nombre_usuario], "add")

                self.solicitar_archivos()

                self.thread_escucha = threading.Thread(target=self.escuchar_servidor, daemon=True)
                self.thread_escucha.start()

            except ConnectionError:
                self.senal_fail.emit('Error de conexión, \nintente nuevamente')
                print('Error de conexión, intente nuevamente')
                self.desconectar()
        else:
            self.senal_fail.emit('Error al ingresar,\nNombre inválido...')
            self.desconectar()

    def escuchar_servidor(self) -> None:
        total = "" # para acumular mensajes largos
        """
        Escucha mensajes del servidor en un bucle infinito.
        """
        while True:
            try:
                if self.socket is None:
                    break
                # Delimitador: |
                respuesta = self.socket.recv(1024).decode('utf-8')
                total += respuesta
                while "|" in total:
                    respuesta, total = total.split("|", 1)

                    if respuesta.startswith("ONLINE:"):
                        usuarios_json = respuesta.split(":", 1)[1].strip("|")
                        usuarios = json.loads(usuarios_json)
                        self.senal_actualizar.emit(usuarios, "add")

                    elif respuesta.startswith("ARCHIVOS:"):
                        archivos_json = respuesta.split(":", 1)[1].strip("|")
                        archivos = json.loads(archivos_json)
                        self.senal_actualizar_archivos.emit(archivos)
                    
                    else:
                        pass
                
            except (ConnectionAbortedError, ConnectionResetError):
                print("Conexión cerrada por el servidor.")
                self.desconectar()
                break
            except OSError as e:
                print(f"Error de socket: {e}")
                self.desconectar()
                break
            except ConnectionError:
                print("Conexión perdida con el servidor.")
                self.desconectar()
                break
    
    def solicitar_descarga(self, nombre_archivo: str) -> None:
        mensaje = f"descargar:{nombre_archivo}"
        print(f"Solicitando archivo: {nombre_archivo}")
        self.socket.sendall(mensaje.encode('utf-8'))
    
    def request(self, msg: str) -> None:
        """
        Envía mensajes al servidor. Enviamos el identificador único que está compuesto por:
        por mientras: nombre de archivo, quien lo tiene (server por ahora) y despues b'\x01'
        """
        msg_bytes = msg.encode('utf-8')
        identificador = bytearray()
        identificador.extend(msg_bytes)
        while len(identificador) != 64:
            identificador.extend(b'\x01')
        self.socket.sendall(identificador)

    def download(self) -> None:
        """
        Inicia el thread para recibir una descarga. Si no hay un thread de descargas, se crea
        """
        if self.thread_descarga is None or not self.thread_descarga.isRunning():
            thread = descargarQThread(self.socket)
            #señales
            thread.start()

    def solicitar_archivos(self):
        self.socket.sendall("lista archivos:".encode('utf-8'))

    def desconectar(self) -> None:
        if self.socket:
            try:
                self.socket.sendall("desconectar".encode())
            except (OSError, ConnectionError):
                print("No se pudo enviar el mensaje de desconexión.")
            finally:
                self.socket.close()
                self.socket = None
                print("Cliente desconectado del servidor.")

        if self.thread_escucha and self.thread_escucha.is_alive():
            self.thread_escucha = None
        
        if self.thread_descarga and self.thread_descarga.is_alive():
            self.thread_descarga = None

class descargarQThread(QThread):
    senal_progreso = pyqtSignal(int)
    senal_completado = pyqtSignal(str)

    def __init__(self, nombre_usuario: str, socket: socket.socket) -> None:
        super().__init__()
        self.socket = socket
        self.user = nombre_usuario

    def run(self) -> None:
        print("Iniciando el thread que recibe una descarga...")

        while True:
            # Contexto
            contexto = self.socket.recv(SIZE_BUFFER)
            id = contexto[:64]
            largo = int.from_bytes(contexto[64:68])
            # Archivo
            file = bytearray()
            bytes_leidos = 0
            while bytes_leidos < largo:
                chunk = self.socket.recv(min(SIZE_BUFFER, largo - bytes_leidos))
                posicion = int.from_bytes(chunk[:3], 'big')
                identificador = chunk[3:69]
                contenido = chunk[posicion:posicion+32]
                bytes_leidos += contenido
                progreso = int((bytes_leidos / largo) * 100)
                self.senal_progreso.emit(progreso)
                print(f"He recibido bytes! Van {bytes_leidos} en total.")
            file.extend(contenido)

            """ruta_archivo = os.path.join(self.carpeta_destino, id_archivo)
            with open(ruta_archivo, 'wb') as file:
                file.write(file_data)

            # Emitir señal de completado
            self.senal_completado.emit(ruta_archivo)
            print(f"Archivo descargado exitosamente: {ruta_archivo}")"""

def validar_usuario(user: str) -> bool:
    mayus = 0
    nums = 0
    if len(user) < 3 or len(user) > 16:
        return False
    for valor in user:
        if not valor.isalnum():
            return False
        if valor.isnumeric():
            nums += 1
        if valor.isupper():
            mayus += 1
    if nums >= 1 and mayus >= 1:
        return True