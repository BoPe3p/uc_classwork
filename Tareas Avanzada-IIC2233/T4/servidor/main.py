import socket
from PyQt5.QtCore import QObject, pyqtSignal
from parametros import (SIZE_BUFFER, NOMBRE_DIRECTORIO, JSON_FILE, COMMAND_1,
                        COMMAND_2, COMMAND_3, COMMAND_4)
import os, sys, threading, json

class Server(QObject):
    senal_new_user = pyqtSignal(str)
    senal_login = pyqtSignal(str, str)

    def __init__(self, port: int, host: str) -> None:
        super().__init__()
        self.clientes = {} # nombre: socket
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
        #Lo anterior es para ver los prints en tiempo real!!

        self.bind_and_listen()
        self.accept_connections()

    def bind_and_listen(self) -> None:
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen()
        except OSError: # Esto es si se intenta instanciar otro server con el mismo port
            print("Intenta con otro port")

    def accept_connections(self) -> None:
        """
        Inicia el thread que aceptará clientes.
        """
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        print("Servidor aceptando conexiones...")
        while True:
            client_socket, _ = self.sock.accept()
            client_name = client_socket.recv(1024).decode('utf-8')
            if client_name in self.clientes:
                client_socket.sendall("Usuario existente".encode('utf-8'))
                client_socket.close()
                continue

            self.clientes[client_name] = client_socket
            # Acá se notifica al cliente de los otros conectados
            usuarios = list(self.clientes.keys())
            usuarios_conectados = json.dumps(usuarios)
            client_socket.sendall(f"ONLINE:{usuarios_conectados}|".encode('utf-8'))
            # Aca se notifica a los otros clientes del nuevo login
            self.broadcast(COMMAND_1)
            print(f"{client_name} conectado. Usuarios: {list(self.clientes.keys())}")

            listening_client_thread = threading.Thread(
                target=self.escuchar_cliente, args=(client_socket, client_name), daemon=True)
            listening_client_thread.start()
            
    # Thread encargado de escuchar a 1 cliente
    def escuchar_cliente(self, client_socket: socket.socket, client_name: str) -> None:
        print("Escuchando clientes...")
        try:
            while True:
                mensaje = client_socket.recv(1024).decode()

                if mensaje.startswith(COMMAND_2):
                    self.cerrar_cliente(client_socket, client_name)
                    print(f"se ha desconectado: {client_name}")
                    break

                elif mensaje.startswith(COMMAND_3):
                    nombre_archivo = mensaje.split(":", 1)[1]
                    self.enviar_archivo(client_socket, nombre_archivo)

                elif mensaje.startswith(COMMAND_4):
                    archivos = self.listar_archivos()
                    archivos_json = json.dumps(archivos)
                    client_socket.sendall(f"ARCHIVOS:{archivos_json}|".encode('utf-8'))

        except ConnectionError:
            self.cerrar_cliente(client_socket, client_name)
            
    def broadcast(self, command):
        """
        Manda un mensaje a todos los sockets conectados.
        """
        if command == COMMAND_1:
            usuarios = list(self.clientes.keys())
            usuarios_conectados = json.dumps(usuarios)
            for client_socket in self.clientes.values():
                print(f"enviando: ONLINE:{usuarios_conectados}|")
                client_socket.sendall(f"ONLINE:{usuarios_conectados}|".encode('utf-8'))

    def listar_archivos(self) -> list:
        """
        Devuelve una lista de archivos disponibles.
        """
        carpeta = NOMBRE_DIRECTORIO  # Carpeta en el servidor
        if not os.path.exists(NOMBRE_DIRECTORIO):
            os.makedirs(carpeta)
        archivos = os.listdir(carpeta)
        return [(archivo, os.path.getsize(os.path.join(carpeta, archivo))) for archivo in archivos]

    def enviar_archivo(self, client_socket: socket.socket, nombre_archivo: str) -> None:
        ruta = os.path.join(NOMBRE_DIRECTORIO, nombre_archivo)
        if os.path.exists(ruta):
            with open(ruta, "rb") as archivo:
                contenido = archivo.read()
            client_socket.sendall(f"ARCHIVO:{nombre_archivo}".encode('utf-8') + contenido)
            print(f"Archivo {nombre_archivo} enviado a {client_socket}.")
        else:
            client_socket.sendall(f"ERROR:Archivo no encontrado|".encode('utf-8'))


    def cerrar_cliente(self, client_socket: socket.socket, client_name: str) -> None:
        if client_name in self.clientes:
            del self.clientes[client_name]
            print(f"se desconecto: {client_name}")
            self.broadcast(COMMAND_1)
        if client_socket:
            client_socket.close()

    def cerrar(self) -> None:
        self.sock.close()


    def get_command(self, identificador: bytearray) -> tuple:
        instrucciones = bytearray(identificador)
        i = instrucciones.index(b'\x01')
        instrucciones = instrucciones[:i]
        instrucciones = instrucciones.decode('utf-8')
        instrucciones = instrucciones.split(",")            
        archivo, propietario = instrucciones[0], instrucciones[1]
        return (archivo, propietario)
    
    @staticmethod
    def send(instruccion: tuple, sock: socket.socket, id: bytearray) -> None:
        """
        Envía mensajes hacia algún socket cliente en chunks de 131 bytes.
        """
        archivo, propietario = instruccion[0], instruccion[1]
        if propietario == 'Servidor':
            ruta = os.path.join(NOMBRE_DIRECTORIO, archivo)
            with open(ruta, 'rb') as file:
                datos = file.read()
                largo_archivo = len(datos)
                # contexto
                contexto = bytearray()
                contexto.extend(id)
                contexto.extend(largo_archivo.to_bytes(4, 'big'))
                contexto.extend(bytearray(63))  # Esto añade 63 bytes con valor 0.
                sock.sendall(contexto)
                # mandar archivo
                bytes_enviados = 0
                while bytes_enviados < largo_archivo:
                    bytes_enviados += sock.send(datos[bytes_enviados:])
    

if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    try:
        port = int(sys.argv[1])
        path = os.path.join(JSON_FILE)
        with open(path) as f:
            data = json.load(f)
        data["port"] = port

        servidor = Server(**data)

    except:
        print("Escribe un port válido \n0-65535")
