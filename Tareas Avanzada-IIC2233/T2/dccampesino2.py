import random
import parametros as prm
import extras as ex
from abc import ABC, abstractmethod

class Plantas(ABC):

    def __init__(self, tipo: str, vida_max: int, vida: int, resistencia: int, resistencia_t: int,
                  congelacion: bool, altura: int) -> None:
                self.tipo = tipo
                self.vida_max = vida_max
                self._vida = vida
                self.resistencia = resistencia
                self.resistencia_t = resistencia_t
                self._congelacion = congelacion
                self.altura = altura
                self.potenciada_p = False #True si está potenciada por Potencilantro
                self.potenciada_c = False #True si está potenciada por Cilantrillo
                self._temperatura = None #Temperatura del jardin
    
    def __str__(self) -> str:
        if self.congelacion:
            return f"*{self.tipo}*"
        else:
            return f"{self.tipo}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_temp(self, temperatura: int) -> None: #Actualiza la t del jardin
        self._temperatura = temperatura

    @property
    def congelacion(self) -> bool:
        if self._temperatura is not None:
            return self._temperatura < self.resistencia_t
        return self._congelacion
    
    @congelacion.setter
    def congelacion(self, value: bool) -> None:
        self._congelacion = value

    @property
    @abstractmethod
    def vida(self) -> int:
        return self._vida
    
    @vida.setter
    @abstractmethod
    def vida(self, value: int) -> None:
        pass

    def regarse(self, num: int, fila: int, columna: int, dificultad: str) -> str:
        old_salud = self.vida
        if dificultad == 'facil':
            if num <= 40:
                self.vida = (prm.RIEGO_1)
            else:
                self.vida = prm.RIEGO_2
        if dificultad == 'media':
            if num <= 60:
                self.vida = (prm.RIEGO_1)
            else:
                self.vida = prm.RIEGO_2
        if dificultad == 'dificil':
            if num <= 70:
                self.vida = (prm.RIEGO_1)
            else:
                self.vida = prm.RIEGO_2
        new_salud = self.vida
        p = f"Un {self.tipo} en ({fila},{columna}) ha subido su salud de {old_salud} a {new_salud}"
        return p

class Solaretillo(Plantas):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo
        self.potencial = random.randint(prm.POTENCIAL_SOLARETILLO_MIN,
                                         prm.POTENCIAL_SOLARETILLO_MAX)
        
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, value: int) -> int:
        life = self.vida
        if (value + life) < 0:
            self._vida = 0
        elif (value + life) > self.vida_max:
            self._vida = self.vida_max
        else:
            self._vida = (value + life)
    
    def producir_soles(self, temp, evento) -> int:
        soles = 0
        if self.congelacion == False:
            if self.potenciada_p == True:
                normal = round(prm.CONSTANTE_SOLES * self.potencial * 
                               (temp / 25) * (self.altura / 30) * (1+ (prm.AUMENTO_NUTRIENTE / 100)))
            if self.potenciada_c == True:
                normal = round(prm.CONSTANTE_SOLES * (1 + prm.AUM_POT_CIL)* self.potencial 
                               * (temp / 25) * (self.altura / 30) * 
                               (1+ ((prm.AUM_AUM_CIL * prm.AUMENTO_NUTRIENTE) / 100)))
            elif self.potenciada_c == False and self.potenciada_p == False:
                normal  = round(prm.CONSTANTE_SOLES * self.potencial * 
                                (temp / 25) * (self.altura / 30))
            if self.vida > 0 and self.congelacion == False:
                if evento == "helada":
                    soles = normal + prm.SOLES_EXTRA_HELADA
                else:
                    soles = normal
        if soles < 0:
            soles *= -1
        return soles

class Defensauce(Plantas):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._armadura = round(self._vida * prm.ARMADURA)
    
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, value: int) -> int:
        life = self.vida
        if self.armadura == 0:
            if (value + life) < 0:
                self._vida = 0
            elif (value + life) > self.vida_max:
                self._vida = self.vida_max
            else:
                self._vida = (value + life)
        else:
            self.armadura += value
    
    @property
    def armadura(self) -> int:
        return self._armadura
    
    @armadura.setter
    def armadura(self, value: int) -> int:
        if value >= 0: #Diferenciamos daño con poner armadura
            self._armadura = value
        else:
            new_armadura = self._armadura + value
            self._armadura = max(new_armadura, 0)

class Potencilantro(Plantas):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.aumento = prm.AUMENTO_NUTRIENTE
    
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, value: int) -> int:
        life = self.vida
        if (value + life) < 0:
            self._vida = 0
        elif (value + life) > self.vida_max:
            self._vida = self.vida_max
        else:
            self._vida = (value + life)
    
    def potenciar(self, tablero_plantas: list, y: int, x: int) -> list:
        tablero = tablero_plantas
        buff = False
        #Cuadrado e = [(x,y)]
        e1 = [(x - 1), (y - 1)]
        e2 = [(x + 1), (y - 1)]
        e3 = [(x - 1), (y + 1)]
        e4 = [(x + 1), (y + 1)]
        esquinas = [e1, e2, e3, e4]
        for e in esquinas:
            e[0] = max(0, min(e[0], len(tablero[0]) - 1))
            e[1] = max(0, min(e[1], len(tablero) - 1))
        if self.congelacion == False:
            buff = True
        for fila in range(len(tablero)):
            for columna in range(len(tablero[0])):
                if fila in range(e1[1], (e3[1] + 1)):
                    if columna in range(e1[0], (e2[0] + 1)):
                        planta = tablero[fila][columna]
                        if planta != "X":
                            if planta.tipo == "S": #Solo potencia Solaretillos
                                planta.potenciada_p = buff
        return tablero
  
class Aresauce(Defensauce, Solaretillo):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class Cilantrillo(Solaretillo, Potencilantro):

    def __init__(self, *args, **kwargs) -> None:
        Solaretillo.__init__(self, *args, **kwargs) 
        Potencilantro.__init__(self, *args, **kwargs) 
        self.potencial = self.potencial * (1 + prm.AUM_POT_CIL)
        self.aumento = self.aumento * (1 + prm.AUM_AUM_CIL)
    
    def potenciar(self, tablero_plantas: list, y: int, x: int) -> list:
        tablero = tablero_plantas
        buff = False
        #Cuadrado e = [(x,y)]
        e1 = [(x - 1), (y - 1)]
        e2 = [(x + 1), (y - 1)]
        e3 = [(x - 1), (y + 1)]
        e4 = [(x + 1), (y + 1)]
        esquinas = [e1, e2, e3, e4]
        for e in esquinas:
            e[0] = max(0, min(e[0], len(tablero[0]) - 1))
            e[1] = max(0, min(e[1], len(tablero) - 1))
        if self.congelacion == False:
            buff = True
        for fila in range(len(tablero)):
            for columna in range(len(tablero[0])):
                if fila in range(e1[1], (e3[1] + 1)):
                    if columna in range(e1[0], (e2[0] + 1)):
                        planta = tablero[fila][columna]
                        targets = ["S", "A", "C"]
                        if planta != "X":
                            if planta.tipo in targets:
                                planta.potenciada_c = buff
        return tablero

class Fensaulantro(Defensauce, Potencilantro):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)