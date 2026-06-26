import random
import parametros as prm
import extras as ex
from dccampesino2 import Solaretillo, Defensauce, Potencilantro
from dccampesino2 import Aresauce, Cilantrillo, Fensaulantro

lista_eventos = ex.lista_eventos
lista_plantas = ex.lista_plantas
lista_jardines = ex.lista_jardines

class Jardin:
    def __init__(self, tablero: list) -> None:
        self.tablero = tablero #Tablero con strings
        self.inventario_plantas = []
        self.soles = prm.SOLES_INICIO
        self.temperatura = prm.TEMP_INICIAL
        tablero_plantas = [] #Tablero con objetos
        plantas_clases = {"S": Solaretillo, "D": Defensauce, "P": Potencilantro, 
                        "A": Aresauce, "C": Cilantrillo, "F": Fensaulantro}
        for fila in tablero:
            fila_plantas = []
            for columna in fila:
                if columna != "X":
                    clase = plantas_clases.get(columna)
                    if clase:
                        s = ex.stats_plantas[columna] #Obtenemos stats del string
                        planta = clase(columna, s[0], s[1], s[2], s[3], s[4], s[5])
                        planta.get_temp(self.temperatura) #Vemos si se congela o no
                        fila_plantas.append(planta)
                else:
                    fila_plantas.append("X")
            tablero_plantas.append(fila_plantas)
        self.tablero_plantas = tablero_plantas
        
    def __str__(self) -> str:
        print("*** Este es tu Jardín ***")
        print(f"Temperatura: {self.temperatura} °C \n")
        for fila in self.tablero_plantas:
            print(f"{fila}")
        print("")
        return f"Inventario Plantas:\n{self.inventario_plantas}"
 
    @property 
    def soles(self) -> int:
         return self._soles
        
    @soles.setter
    def soles(self, value: int) -> int:
        if value < 0:
            value = 0
        else:
             value = int(value)
        self._soles = value

    def cultivar_planta(self, tipo: int, coordenada_y: int, coordenada_x: str) -> None:
        inventario = self.inventario_plantas
        tablero = self.tablero
        tablero_plantas = self.tablero_plantas
        for i in range(len(inventario)):
            if inventario[i].tipo == tipo:
                index = i
        planta = inventario.pop(index) #Sacamos la planta del inventario
        tablero[coordenada_y][coordenada_x] = tipo
        tablero_plantas[coordenada_y][coordenada_x] = planta
        self.tablero = tablero
        self.tablero_plantas = tablero_plantas
        self.inventario_plantas = inventario
        return

    def regar_plantas(self, dificultad: str) -> None: 
        soles = self.soles
        if soles >= 10:
            print(ex.print_regar)
            tablero = self.tablero_plantas
            for fila in range(len(tablero)):
                for columna in range(len(tablero[0])):
                    if tablero[fila][columna] != "X":
                        planta = tablero[fila][columna] 
                        num = random.randint(0,100)
                        p = planta.regarse(num, fila, columna, dificultad)
                        print(p)
            self.tablero_plantas = tablero
            self.soles = (soles - 10)
        else:
            print("No tienes soles suficientes para regar")
        return 

    def calcular_soles(self, evento: str) -> None:
        tablero = self.tablero_plantas
        sol = self.soles
        soles = 0
        prod = 0
        cielo = random.randint(prm.MIN_SOLES, prm.MAX_SOLES)
        print(ex.print_soles)
        for fila in range(len(tablero)):
            for columna in range(len(tablero[0])):
                if tablero[fila][columna] != "X":
                    if tablero[fila][columna].tipo in ["S", "A", "C"]:
                        planta = tablero[fila][columna]
                        soles = planta.producir_soles(self.temperatura, evento)
                        prod += soles
                        print(f"Un {planta.tipo} en ({fila},{columna}) ha producido {soles} soles")
                        print(ex.print_espacio)
        print(f"Se han obtenido {cielo} soles del cielo\n")
        prod += cielo
        print(f"En total se han recolectado {prod} soles durante el dia")
        sol += prod
        self.soles = sol
        return 

    def mutar(self, tipo) -> None:
        inventario = self.inventario_plantas
        plantits = [planta.tipo for planta in inventario]
        stats = ex.stats_plantas
        if tipo == "A":
            if "S" in plantits and "D" in plantits:
                index = plantits.index("S")
                plantits.pop(index)
                inventario.pop(index)
                index = plantits.index("D")
                plantits.pop(index)
                inventario.pop(index)
                a = stats["A"]
                mutada = Aresauce("A", int(a[0]), int(a[1]), int(a[2]),
                                     int(a[3]), bool(a[4]), int(a[5]))
                inventario.append(mutada)
                self.inventario_plantas = inventario
            else:
                print("No se tiene una o las dos plantas necesarias para mutar :(")
        elif tipo == "C":
            if "S" in plantits and "P" in plantits:
                index = plantits.index("S")
                plantits.pop(index)
                inventario.pop(index)
                index = plantits.index("P")
                plantits.pop(index)
                inventario.pop(index)
                a = stats["C"]
                mutada = Aresauce("C", int(a[0]), int(a[1]), int(a[2]),
                                     int(a[3]), bool(a[4]), int(a[5]))
                inventario.append(mutada)
                self.inventario_plantas = inventario
            else:
                print("No se tiene una o las dos plantas necesarias para mutar :(")
        elif tipo == "F":
            if "P" in plantits and "D" in plantits:
                index = plantits.index("P")
                plantits.pop(index)
                inventario.pop(index)
                index = plantits.index("D")
                plantits.pop(index)
                inventario.pop(index)
                a = stats["F"]
                mutada = Aresauce("F", int(a[0]), int(a[1]), int(a[2]),
                                     int(a[3]), bool(a[4]), int(a[5]))
                inventario.append(mutada)
                self.inventario_plantas = inventario
            else:
                print("No se tiene una o las dos plantas necesarias para mutar :(")
        return

    def presentarse(self):
        print(self)
        return
    
    def intercambiar(self, coords: str) -> None:
        tablero = self.tablero
        tablero_p = self.tablero_plantas
        coords = coords.split(";")
        c1 = coords[0].split(",") #Listas con las coords
        c1y = int(c1[0])
        c1x = int(c1[1])
        c2 = coords[1].split(",")
        c2y = int(c2[0])
        c2x = int(c2[1])
        alto = len(tablero) -1
        ancho = len(tablero[0]) -1
        if (0 <= c1y <= alto and 0 <= c1x <= ancho and 
            0 <= c2y <= alto and 0 <= c2x <= ancho):
                tablero[c1y][c1x], tablero[c2y][c2x] = tablero[c2y][c2x], tablero[c1y][c1x]
                tablero_p[c1y][c1x], tablero_p[c2y][c2x] = tablero_p[c2y][c2x], tablero_p[c1y][c1x]
                self.tablero = tablero
                self.tablero_plantas = tablero_p
                return
        else:
            print("Coordenadas invalidas")
            return
