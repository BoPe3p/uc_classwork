import parametros as prm
import extras as ex
import random
from dccampesino import Jardin, Solaretillo, Defensauce, Potencilantro
from dccampesino import Aresauce, Cilantrillo, Fensaulantro

def pasar_dia(jardin: object, dificultad: str) -> int:
    dia = 1
    tp = jardin.tablero_plantas
    alto = len(tp)
    ancho = len(tp[0])
    # 0. Temperatura
    new_temp = random.randint(prm.TEMP_MIN_JARDIN, prm.TEMP_MAX_JARDIN)
    jardin.temperatura = new_temp
    for fila in tp:
        for col in fila:
            if col != "X":
                col.get_temp(new_temp)
    # 1. Aplicar buffs/debuffs
    for fila in tp:
        for col in fila:
            if col != "X":
                col.potenciada_p = False #Sacamos el buff por si murieron los potenciadores
                col.potenciada_c = False
    hay_F = False
    hay_A = False
    for fila in jardin.tablero:
        for col in fila:
            if col == "F":
                hay_F = True
            if col == "A":
                hay_A = True
    for fila in range(len(tp)):
        for col in range(len(tp[0])):
            potenciadores = ["P", "C", "F"]
            planta = tp[fila][col]
            if planta != "X":
                if planta.tipo in potenciadores:
                    try: #Me estaba dando un error extraño
                        tp = planta.potenciar(tp, fila, col)
                    except:
                        pass
    jardin.tablero_plantas = tp
    # 2. Evento
    lista_eventos = ex.lista_eventos
    if dificultad == "facil":
        index = 1
    elif dificultad == "media":
        index = 2
    elif dificultad == "dificil":
        index = 3
    elegido = "NONE"
    for event in lista_eventos: #Elegimos máximo 1 evento
        num = random.randint(1, 100)
        if elegido == "NONE":
            if num <= (float(event[index]) * 100):
                elegido = event[0]
    if elegido == "NONE":
        print(ex.tranquilo)
        new_temp = random.randint(prm.TEMP_MIN_TRANQUI, prm.TEMP_MAX_TRANQUI)
        jardin.temperatura = new_temp
        for fila in tp:
            for col in fila:
                if col != "X":
                    col.get_temp(new_temp)
    elif elegido == "Z":
        print(ex.oleada)
        if dificultad == "facil":
            z = prm.ZOMBIES_FACIL
            ataque = 10
        elif dificultad == "media":
            z = prm.ZOMBIES_MEDIA
            ataque = 20
        elif dificultad == "dificil":
            z = prm.ZOMBIES_DIFICIL
            ataque = 30
        i = 0
        soles = 0
        if hay_F == True:
            debuff = prm.RED_ATQ
        for rep in range(z):
            y = random.randint(0, (alto -1))
            x = random.randint(0, (ancho -1))
            if tp[y][x] == "X":
                print(f"¡Un zombie intentó atacar la posición {(x, y)} pero estaba vacía")
            else:
                i += 1
                planta = tp[y][x]
                if hay_F:
                    daño = max(1, round(((1 - debuff) * ataque) * ((40 - planta.resistencia)/ 40)))
                else:
                    daño = max(1, round(ataque * ((40 - planta.resistencia)/ 40)))
                planta.vida = (-1 * daño)
                print(f"La planta {planta.tipo} en {(x, y)} ha perdido {daño} puntos de vida")
                if planta.vida == 0:
                    print("Este ataque acabó con su vida. RIP")
                    planta = "X" #Las plantas que mueren se quitan automáticamente
                tp[y][x] = planta
                if hay_A:
                    soles += (1 - prm.ANTI_ROBO) * prm.SOLES_ROBADOS #Robamos los soles con debuff
                    soles = round(soles)
                else:
                    soles += prm.SOLES_ROBADOS #Robamos los soles
        if i > 0:
            print(f"Los zombies lograron atacar {i} casillas, robando {soles} soles")
            old = jardin.soles
            jardin.soles = (old - soles)
        else:
            print("¡Ninguna de tus plantas fue atacada! No has sufrido robos de soles")
    elif elegido == "H":
        print(ex.helada)
        new_temp = random.randint(prm.TEMP_MIN_HELADA, prm.TEMP_MAX_HELADA)
        jardin.temperatura = new_temp
        for fila in tp:
            for col in fila:
                if col != "X":
                    col.get_temp(new_temp)
    # 3. Calcular soles
    jardin.calcular_soles(elegido)
    # 4. Llegada de plantas
    num = random.randint(prm.NUM_MIN_PLANTA, prm.NUM_MAX_PLANTA)
    print(f"*** Han llegado {num} plantas a tu inventario ***")
    basicas = ["S", "D", "P"]
    stats = ex.stats_plantas
    llegada = []
    for i in range(num):
        index = random.randint(0, 2)
        tipo = basicas[index]
        vm, v, r = stats[tipo][0], stats[tipo][1], stats[tipo][2]
        rt, c, a = stats[tipo][3], stats[tipo][4], stats[tipo][5]
        if tipo == "S":
            planta = Solaretillo(tipo, vm, v, r, rt, c, a)
        elif tipo == "D":
            planta = Defensauce(tipo, vm, v, r, rt, c, a)
        elif tipo == "P":
            planta = Potencilantro(tipo, vm, v, r, rt, c, a)
        llegada.append(planta)
    sumar = jardin.inventario_plantas #Inventario con objetos, no str
    jardin.inventario_plantas = sumar + llegada
    # 5. Presentacion
    print(jardin) # Llama al metodo __str__
    return dia
