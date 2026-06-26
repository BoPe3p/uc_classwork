import os

def ordenar(lista: list) -> tuple:
    return lista[1] , lista[0]

class Predio:
    def __init__(self, codigo_predio: str, alto: int, ancho: int) -> None:
        self.codigo_predio = codigo_predio
        self.alto = alto
        self.ancho = ancho
        self.plano = []
        self.plano_riego = []

    def crear_plano(self, tipo: str) -> None:
        filas = self.alto
        columnas = self.ancho
        plano = self.plano
        plano_riego = self.plano_riego
        if tipo.lower() == "normal": #Uso lower() para que sea en minúscula
            for i in range(filas):
                lista = ["X"] * columnas
                plano.append(lista)
            self.plano = plano
        elif tipo.lower() == "riego":
            for i in range(filas):
                lista = [0] * columnas
                plano_riego.append(lista)
            self.plano_riego = plano_riego
        return

    def plantar(
        self, codigo_cultivo: int, coordenadas: list, alto: int, ancho: int
    ) -> None:
        plano = self.plano
        filas = self.alto
        columnas = self.ancho
        f = coordenadas[0]
        c = coordenadas[1]
        cultivos_a_plantar = int(alto) * int(ancho) #Número máximo a plantar
        plantados = 0
        for n in range(filas):
            for m in range(columnas):
                if n == f and m == c:
                    for i in range(ancho):
                        plano[n][m+i] = codigo_cultivo
                        plantados += 1
                    if plantados == cultivos_a_plantar:
                        self.plano = plano
                        return
                    f += 1
        return

    def regar(self, coordenadas: list, area: int) -> None:
        plano = self.plano_riego
        filas = self.alto
        columnas = self.ancho
        # Esquinas
        e1 = [(coordenadas[0] - area), (coordenadas[1] - area)]
        e2 = [(coordenadas[0] - area), (coordenadas[1] + area)]
        e3 = [(coordenadas[0] + area), (coordenadas[1] - area)]
        e4 = [(coordenadas[0] + area), (coordenadas[1] + area)]
        esquinas = [e1, e2, e3, e4]
        for e in esquinas:
            if e[0] < 0:
                e[0] = 0
                e.append(True) # Si se sale del predio
            if e[0] > (filas - 1):
                e[0] = filas
                e.append(True)
            if e[1] < 0:
                e[1] = 0
                e.append(True)
            if e[1] > (columnas - 1):
                e[1] = columnas
                e.append(True)
        # Regamos el predio
        for fila in range(filas):
            for columna in range(columnas):
                if fila in range(e1[0], (e3[0] + 1)):
                    if columna in range(e1[1], (e2[1] + 1)):
                        plano[fila][columna] += 1
                        f = plano[fila]
        # Quitamos las esquinas
        for e in esquinas:
            if len(e) == 2:
                plano[e[0]][e[1]] -= 1
        self.plano_riego = plano
        return

    def eliminar_cultivo(self, codigo_cultivo: int) -> int:
        eliminadas = 0
        plano = self.plano
        filas = self.alto
        columnas = self.ancho
        for n in range(filas):
            for m in range(columnas):
                cultivo = "Variable"
                tipo = type(plano[n][m])
                if tipo == int:
                    cultivo = int(plano[n][m])
                if cultivo == codigo_cultivo:
                    plano[n][m] = "X"
                    eliminadas += 1
        self.plano = plano
        return eliminadas

class DCCultivo:
    def __init__(self) -> None:
        self.predios = []

    def crear_predios(self, nombre_archivo: str) -> str:
        ruta = os.path.join("data", nombre_archivo)
        comprobar = os.path.exists(ruta) # Comprobamos si la ruta es válida
        if comprobar == True:
            with open(ruta, "rt") as archivo:
                lineas = archivo.readlines()
            for i in range(len(lineas)):
                lineas[i] = lineas[i].strip().split(',') #Eliminamos \n
            for predio in lineas:
                codigo = predio[0]
                alto = int(predio[1])
                ancho = int(predio[2])
                add = Predio(codigo, alto, ancho) # Generamos el objeto
                add.crear_plano("normal")
                add.crear_plano("riego")
                self.predios.append(add)
            return "Predios de DCCultivo cargados exitosamente"
        elif comprobar == False:
            return "Fallo en la carga de DCCultivo"

    def buscar_y_plantar(self, codigo_cultivo: int, alto: int, ancho: int) -> bool:
        # Filtramos predios
        validos = []
        for i in range(len(self.predios)):
            predio = self.predios[i]
            plano = predio.plano
            contador = 0
            for row in plano:
                if codigo_cultivo not in row:
                    contador += 1
            if contador == predio.alto:
                validos.append(predio)
        # Entre los validos buscamos y plantamos
        plantar = ancho * alto
        plantadas = 0
        buscar = ["X"] * ancho
        for predio in validos:
            plano = predio.plano
            field = predio
            fila = 0
            col = 0
            while plantadas != plantar:
                if (col + ancho) > predio.ancho:
                    plantadas = 0
                    col = 0
                    fila += 1
                if (fila + alto) > predio.alto:
                    break
                bloque = plano[fila][col: col + ancho]
                if bloque == buscar:
                    if plantadas == 0:
                        fp = fila
                        cp = col
                    for i in range(alto):
                        bloque = plano[fila + i][col: col + ancho]
                        if bloque != buscar:
                            plantadas = 0
                            col += 1
                            break
                        elif bloque == buscar:
                            plantadas = plantadas + (1 * ancho)
                elif bloque != buscar:
                    plantadas = 0
                    col += 1
            if plantadas == plantar:
                field.plantar(codigo_cultivo, [fp, cp], alto, ancho)
                return True
        return False

    def buscar_y_regar(self, codigo_predio: str, coordenadas: list, area: int) -> None:
        lista = self.predios
        for predio in lista:
            if predio.codigo_predio == codigo_predio:
                predio.regar(coordenadas, area)
        return

    def detectar_plagas(self, lista_plagas: list[list]) -> list[list]:
        lista = []
        for plaga in lista_plagas:
            codigo = plaga[0]
            coords = plaga[1]
            for predio in self.predios: #Filtramos los predios por código
                if predio.codigo_predio == codigo:
                    plano = predio.plano
                    p = predio
                    codigo_cultivo = plano[int(coords[0])][int(coords[1])]
                    if codigo_cultivo != "X":
                        codigo_cultivo = int(codigo_cultivo)
                        eliminadas = p.eliminar_cultivo(codigo_cultivo)
                    elif codigo_cultivo == "X":
                        eliminadas = 0
                    if eliminadas > 0:
                        lista.append([str(codigo), int(eliminadas)])
        # Vemos si se operó en un mismo predio más de 1 vez
        codigos = []
        elim = []
        for field in lista:
            if field[0] not in codigos:
                codigos.append(field[0])
                elim.append(field[1])
            elif field[0] in codigos:
                index = codigos.index(field[0])
                elim[index] = elim[index] + int(field[1])
        lista = []
        for i in range(len(codigos)):
            lista.append([str(codigos[i]), int(elim[i])])
        ordenada = sorted(lista, key = ordenar)
        return ordenada